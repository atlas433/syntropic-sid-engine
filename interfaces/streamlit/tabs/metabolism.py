import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from decimal import Decimal

from application.dto.simulation_dto import SimulationStepDTO


def render_metabolism(simulation_data: list[SimulationStepDTO]):
    st.markdown("### Metabolism — Biomass Flow & Nutrient Cycling")

    if not simulation_data:
        st.info("No simulation data available. Run the simulation first.")
        return

    months = [s.month for s in simulation_data]
    a_prod = [float(s.a_row_biomass_produced_kg) for s in simulation_data]
    c_demand = [float(s.c_row_biomass_demand_kg) for s in simulation_data]
    bioavailable = [float(s.bioavailable_biomass_kg) for s in simulation_data]
    surplus = [float(s.surplus_kg) for s in simulation_data]
    deficit = [float(s.deficit_kg) for s in simulation_data]
    ratios = [float(s.surplus_ratio) if float(s.surplus_ratio) < 99 else 99 for s in simulation_data]
    health_statuses = [s.health_status for s in simulation_data]

    c1, c2, c3 = st.columns(3)
    latest = simulation_data[-1]
    with c1:
        st.metric("A-Row Biomass Produced", f"{float(latest.a_row_biomass_produced_kg):.0f} kg",
                  delta=f"Month {latest.month}")
    with c2:
        st.metric("C-Row Nutrient Demand", f"{float(latest.c_row_biomass_demand_kg):.0f} kg")
    with c3:
        st.metric("Bioavailable Biomass", f"{float(latest.bioavailable_biomass_kg):.0f} kg",
                  delta=f"{float(latest.surplus_ratio):.2f}x ratio")

    st.markdown("---")

    st.markdown("#### Production vs Demand (Sankey-Style Flow)")
    fig_flow = make_subplots(specs=[[{"secondary_y": True}]])

    fig_flow.add_trace(go.Bar(
        x=months, y=a_prod, name="A-Row Production",
        marker_color="#2d6a4f", opacity=0.8,
    ), secondary_y=False)

    fig_flow.add_trace(go.Bar(
        x=months, y=c_demand, name="C-Row Demand",
        marker_color="#e07a5f", opacity=0.6,
    ), secondary_y=False)

    fig_flow.add_trace(go.Scatter(
        x=months, y=ratios, name="Surplus Ratio",
        mode="lines+markers", line=dict(color="#3d405b", width=2.5),
        marker=dict(size=6), yaxis="y2",
    ), secondary_y=True)

    fig_flow.add_hline(y=1.2, line_dash="dash", line_color="#059669",
                       annotation_text="Regenerative", secondary_y=True)
    fig_flow.add_hline(y=1.0, line_dash="dash", line_color="#2563eb",
                       annotation_text="Sustainable", secondary_y=True)

    fig_flow.update_layout(
        height=350, template="plotly_white",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Month",
        legend=dict(orientation="h", y=1.1),
        hovermode="x unified",
    )
    fig_flow.update_yaxes(title_text="Biomass (kg)", secondary_y=False)
    fig_flow.update_yaxes(title_text="Surplus Ratio", secondary_y=True)

    st.plotly_chart(fig_flow, use_container_width=True)

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Nutrient Flow Breakdown")
        fig_sankey = go.Figure()

        a_total = sum(a_prod)
        c_total = sum(c_demand)
        bio_total = sum(bioavailable)
        surp_total = sum(surplus)
        def_total = sum(deficit)
        max_val = max(a_total, c_total, bio_total, surp_total + def_total, 1)

        labels = ["A-Row Production", "Decomposition\n(85% rate)", "Loss to Soil OM",
                  "Available to C-Rows", "C-Row Uptake", "Surplus", "Deficit"]
        source = [0, 0, 2, 2, 2]
        target = [1, 2, 3, 4, 5]
        value = [bio_total, a_total - bio_total, bio_total, c_total, surp_total]

        fig_sankey.add_trace(go.Sankey(
            node=dict(
                pad=15, thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=["#2d6a4f", "#40916c", "#74c69d",
                       "#52b788", "#e07a5f", "#059669", "#dc2626"],
            ),
            link=dict(
                source=source, target=target, value=value,
                color=["rgba(45,106,79,0.4)", "rgba(116,198,157,0.3)",
                       "rgba(82,183,136,0.4)", "rgba(224,122,95,0.4)",
                       "rgba(5,150,105,0.3)"],
            ),
        ))
        fig_sankey.update_layout(
            height=300, template="plotly_white",
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_sankey, use_container_width=True)

    with right:
        st.markdown("#### Metabolic Health Distribution")
        status_order = ["REGENERATIVE", "SUSTAINABLE", "STRAINED", "MINING"]
        status_counts = {s: health_statuses.count(s) for s in status_order}
        fig_pie = go.Figure(go.Pie(
            labels=list(status_counts.keys()),
            values=list(status_counts.values()),
            marker_colors=["#059669", "#2563eb", "#d97706", "#dc2626"],
            hole=0.4, textinfo="label+value",
        ))
        fig_pie.update_layout(
            height=300, template="plotly_white",
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    st.markdown("#### Monthly Metabolic Log")
    log_data = [
        {
            "Month": s.month, "A Prod (kg)": f"{float(s.a_row_biomass_produced_kg):.1f}",
            "C Demand (kg)": f"{float(s.c_row_biomass_demand_kg):.1f}",
            "Bioavailable (kg)": f"{float(s.bioavailable_biomass_kg):.1f}",
            "Surplus (kg)": f"{float(s.surplus_kg):.1f}",
            "Ratio": f"{float(s.surplus_ratio):.2f}",
            "Status": s.health_status,
        }
        for s in simulation_data
    ]
    st.dataframe(log_data, use_container_width=True, height=250)

    st.caption("Decomposition rate: **85%** | Default C-Row demand: **8.0 kg/m** | Pruning months: **0, 3, 6, 9, 12** for A-rows")
