import streamlit as st
import plotly.graph_objects as go
import numpy as np
from decimal import Decimal

from application.dto.row_dto import LayoutDTO


def render_strata_3d(layout: LayoutDTO):
    st.markdown("### 3D Strata Visualization — Canopy Heights & Vertical Structure")

    try:
        import pyvista as pv
        pv.OFF_SCREEN = True
        _has_pyvista = True
    except ImportError:
        _has_pyvista = False

    all_plants = [p for r in layout.rows for p in r.plants]
    if not all_plants:
        st.info("No plants loaded")
        return

    strata_colors = {
        "EMERGENT": "#1b4332",
        "HIGH": "#2d6a4f",
        "MEDIUM": "#52b788",
        "LOW": "#95d5b2",
        "GROUND_COVER": "#b7e4c7",
    }

    strata_ordered = ["EMERGENT", "HIGH", "MEDIUM", "LOW", "GROUND_COVER"]
    all_rows = sorted(layout.rows, key=lambda r: r.id)

    fig_go = go.Figure()

    for i, row in enumerate(all_rows):
        y_pos = i * float(layout.row_spacing_m)
        row_color = "#2d6a4f" if row.row_type == "A" else "#e07a5f"

        for j, plant in enumerate(row.plants):
            if j % max(1, len(row.plants) // 12) != 0:
                continue
            x_pos = float(row.length_m) * (j / max(len(row.plants) - 1, 1)) if len(row.plants) > 1 else float(row.length_m) * 0.5
            h = float(plant.current_height_m)
            radius = float(_species_stratum_canopy(plant.stratum))
            stratum = plant.stratum
            color = strata_colors.get(stratum, "#6b7280")
            canopy_z = h * 0.85

            theta = np.linspace(0, 2 * np.pi, 16)
            canopy_x = [x_pos + radius * float(np.cos(t)) for t in theta]
            canopy_y = [y_pos + radius * float(np.sin(t)) for t in theta]

            fig_go.add_trace(go.Scatter3d(
                x=[x_pos, x_pos], y=[y_pos, y_pos], z=[0, h],
                mode="lines", line=dict(color="#8B4513", width=3),
                showlegend=False,
            ))

            fig_go.add_trace(go.Mesh3d(
                x=canopy_x, y=canopy_y,
                z=[canopy_z] * len(canopy_x),
                color=color, opacity=0.6, alphahull=0,
                name=f"{plant.species_name} ({stratum})",
                hovertext=f"{plant.species_name}<br>Height: {h:.1f}m<br>{stratum}",
                showlegend=False,
            ))

    for i, row in enumerate(all_rows):
        y_pos = i * float(layout.row_spacing_m)
        length = float(row.length_m)
        outline_color = "#2d6a4f" if row.row_type == "A" else "#d4a574"
        fig_go.add_trace(go.Scatter3d(
            x=[0, length, length, 0, 0],
            y=[y_pos, y_pos, y_pos + 2, y_pos + 2, y_pos],
            z=[0, 0, 0, 0, 0],
            mode="lines",
            line=dict(color=outline_color, width=2),
            name=row.id, showlegend=True,
        ))

    fig_go.update_layout(
        title="3D Canopy Structure — Emergent to Ground Cover",
        scene=dict(
            xaxis_title="Length (m)", yaxis_title="Width (m)", zaxis_title="Height (m)",
            aspectmode="data",
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
        ),
        height=600,
        template="plotly_white",
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    )

    st.plotly_chart(fig_go, use_container_width=True)

    st.markdown("---")

    st.markdown("### Strata Cross-Section")
    selected_row_id = st.selectbox(
        "Select a row to view cross-section",
        [r.id for r in layout.rows],
    )
    selected_row = next((r for r in layout.rows if r.id == selected_row_id), None)

    if selected_row and selected_row.plants:
        fig_section = go.Figure()
        for j, plant in enumerate(selected_row.plants):
            if j % max(1, len(selected_row.plants) // 20) != 0:
                continue
            x_pos = float(selected_row.length_m) * (j / max(len(selected_row.plants) - 1, 1)) if len(selected_row.plants) > 1 else float(selected_row.length_m) * 0.5
            h = float(plant.current_height_m)
            radius = float(_species_stratum_canopy(plant.stratum)) * 0.8
            color = strata_colors.get(plant.stratum, "#6b7280")

            fig_section.add_shape(
                type="circle", xref="x", yref="y",
                x0=x_pos - radius, y0=h * 0.85 - radius * 0.5,
                x1=x_pos + radius, y1=h * 0.85 + radius * 0.5,
                fillcolor=color, opacity=0.3, line=dict(color=color, width=1),
            )
            fig_section.add_trace(go.Scatter(
                x=[x_pos], y=[h],
                mode="markers+text",
                marker=dict(size=8, color=color),
                text=[plant.species_name[:6]],
                textposition="top center",
                hovertext=f"{plant.species_name}<br>H: {h:.1f}m<br>{plant.stratum}",
                showlegend=False,
            ))

        fig_section.update_layout(
            title=f"Cross-Section: {selected_row_id} ({selected_row.row_type}-Row)",
            height=350, template="plotly_white",
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Position along row (m)",
            yaxis_title="Height (m)",
        )
        st.plotly_chart(fig_section, use_container_width=True)

    st.caption("Height indicators: **Emergent** (>8m) | **High** (4–8m) | **Medium** (1.5–4m) | **Low** (0.3–1.5m) | **Ground Cover** (<0.3m)")


def _species_stratum_canopy(stratum: str) -> Decimal:
    radii = {
        "EMERGENT": Decimal("7.5"),
        "HIGH": Decimal("4.0"),
        "MEDIUM": Decimal("2.0"),
        "LOW": Decimal("1.0"),
        "GROUND_COVER": Decimal("0.75"),
    }
    return radii.get(stratum, Decimal("1.5"))
