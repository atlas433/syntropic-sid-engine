import streamlit as st
import plotly.graph_objects as go
from shapely.geometry import Polygon, Point
from shapely import affinity
import random

from application.dto.row_dto import LayoutDTO


def render_layout_2d(layout: LayoutDTO):
    st.markdown("### 2D Field Layout — Shapely Polygon Visualization")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Field Width", f"{float(layout.field_width_m):.0f} m")
    with c2:
        st.metric("Field Length", f"{float(layout.field_length_m):.0f} m")
    with c3:
        st.metric("Row Spacing", f"{float(layout.row_spacing_m):.0f} m")

    a_rows = [r for r in layout.rows if r.row_type == "A"]
    c_rows = [r for r in layout.rows if r.row_type == "C"]

    fig = go.Figure()

    all_rows = sorted(layout.rows, key=lambda r: r.id)
    for i, row in enumerate(all_rows):
        y_offset = i * float(layout.row_spacing_m)
        length = float(row.length_m)
        row_width = 1.5 if row.row_type == "A" else 2.5
        color = "#2d6a4f" if row.row_type == "A" else "#e07a5f"
        opacity = 0.5 if row.row_type == "A" else 0.4

        rect = Polygon([
            (0, y_offset), (length, y_offset),
            (length, y_offset + row_width), (0, y_offset + row_width),
        ])
        x, y = rect.exterior.xy
        fig.add_trace(go.Scatter(
            x=list(x), y=list(y), fill="toself", mode="lines",
            name=row.id, line=dict(color=color, width=1.5),
            fillcolor=color, opacity=opacity,
            text=f"{row.id} ({row.row_type})<br>{row.plant_count} plants<br>{row.length_m}m",
            hoverinfo="text",
        ))

        for j, plant in enumerate(row.plants):
            if j % max(1, row.plant_count // 15) != 0:
                continue
            x_pos = float(row.length_m) * (j / max(row.plant_count - 1, 1)) if row.plant_count > 1 else float(row.length_m) * 0.5
            y_pos = y_offset + row_width / 2

            h = float(plant.current_height_m)
            plant_color = {
                "EMERGENT": "#1b4332", "HIGH": "#2d6a4f",
                "MEDIUM": "#52b788", "LOW": "#95d5b2",
                "GROUND_COVER": "#b7e4c7",
            }.get(plant.stratum, "#6b7280")
            marker_size = min(18, max(4, h * 2.5))

            fig.add_trace(go.Scatter(
                x=[x_pos], y=[y_pos], mode="markers",
                marker=dict(size=marker_size, color=plant_color, line=dict(width=1, color="white")),
                text=f"{plant.species_name}<br>Height: {h:.1f}m<br>Age: {plant.age_months}mo<br>Stratum: {plant.stratum}",
                hoverinfo="text", showlegend=False,
            ))

    fig.update_layout(
        title="A-Rows (Biomass Production) | C-Rows (Cash Crops)",
        height=500,
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(title="Length (m)", showgrid=True, zeroline=False),
        yaxis=dict(title="Width (m)", showgrid=True, zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="closest",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("#### A-Rows (Biomass Engine)")
        for row in a_rows:
            with st.expander(f"{row.id} — {row.plant_count} plants, {float(row.length_m):.0f}m"):
                st.write(f"Biomass production: **{float(row.biomass_production_kg_per_month):.1f} kg/month**")
                st.write(f"Soil OM: **{float(row.soil_organic_matter_kg_per_m):.1f} kg/m**")
                strata_counts = {}
                for p in row.plants:
                    s = p.stratum
                    strata_counts[s] = strata_counts.get(s, 0) + 1
                st.write("Strata: " + ", ".join(f"{k} ({v})" for k, v in strata_counts.items()))

    with c_right:
        st.markdown("#### C-Rows (Production)")
        for row in c_rows:
            with st.expander(f"{row.id} — {row.plant_count} plants, {float(row.length_m):.0f}m"):
                st.write(f"Nutrient demand: **{float(row.biomass_demand_kg_per_month):.1f} kg/month**")
                st.write(f"Soil OM: **{float(row.soil_organic_matter_kg_per_m):.1f} kg/m**")
                strata_counts = {}
                for p in row.plants:
                    s = p.stratum
                    strata_counts[s] = strata_counts.get(s, 0) + 1
                st.write("Strata: " + ", ".join(f"{k} ({v})" for k, v in strata_counts.items()))
