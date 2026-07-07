import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from application.dto.dashboard_dto import DashboardMetrics
from interfaces.streamlit.components.styles import HEALTH_COLORS, HEALTH_ICONS


def render_dashboard(metrics: DashboardMetrics, network_params: dict, current_month: int):
    icon = HEALTH_ICONS.get(metrics.health_status, "⚪")
    color = HEALTH_COLORS.get(metrics.health_status, "#6b7280")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f"<div style='font-size:1.5rem;font-weight:700;color:{color};'>"
            f"{icon} System Status: {metrics.health_status}</div>",
            unsafe_allow_html=True,
        )
        st.caption(f"Current simulation month: **{metrics.current_month}** | SiD Cycle: **{metrics.cycle_number}**")

    with col2:
        surplus_pct = float(metrics.surplus_ratio) * 100 - 100 if float(metrics.surplus_ratio) < 99 else 9999
        st.metric("Biomass Surplus Ratio", f"{float(metrics.surplus_ratio):.2f}x",
                  delta=f"{surplus_pct:+.0f}% surplus" if surplus_pct < 9000 else "No demand")

    st.markdown("---")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi_card("A-Rows", str(metrics.total_a_rows), "rows", "#2d6a4f")
    with c2:
        kpi_card("C-Rows", str(metrics.total_c_rows), "rows", "#40916c")
    with c3:
        kpi_card("Total Plants", str(metrics.total_plants), "individuals", "#52b788")
    with c4:
        kpi_card("Species", str(metrics.total_species), "unique", "#74c69d")
    with c5:
        kpi_card("Biomass Prod.", f"{float(metrics.a_row_biomass_produced_kg):.0f}", "kg/month", "#1b4332")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Biomass Demand", f"{float(metrics.c_row_biomass_demand_kg):.0f}", "kg/month", "#e07a5f")
    with c2:
        kpi_card("Soil OM", f"{float(metrics.soil_organic_matter_kg_per_m):.1f}", "kg/m", "#81b29a")
    with c3:
        kpi_card("Diversity", f"{float(metrics.diversity_shannon_index):.2f}", "Shannon H", "#3d405b")
    with c4:
        kpi_card("Circularity", f"{float(metrics.circularity):.0%}", "closed loop", "#e07a5f")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.markdown("### Species Library")
        species_data = [
            {"Species": s["name"], "Stratum": s["stratum"], "Succession": s["succession"],
             "Row": s["row_type"], "N-Fixer": "✓" if s["n_fixer"] else "", "Biomass": f"{s['biomass_kg_m_year']:.1f}"}
            for s in metrics.species_list
        ]
        st.dataframe(species_data, use_container_width=True, height=280,
                     column_config={"Species": st.column_config.TextColumn(width="medium")})

        st.markdown("### Performative Goals")
        for g in metrics.goals:
            with st.expander(f"{g['name']} ({g['level']} | {g['elsi']})"):
                st.write(g["description"])
                if g["kpis"]:
                    for k in g["kpis"]:
                        st.caption(f"KPI: **{k['name']}** → `{k['target']}` ({k['unit']})")

    with right:
        st.markdown("### Strata Distribution")
        strata = metrics.strata_distribution
        if sum(strata.values()) > 0:
            fig_strata = go.Figure(go.Bar(
                x=list(strata.keys()), y=list(strata.values()),
                marker_color=["#1b4332", "#2d6a4f", "#40916c", "#52b788", "#74c69d"],
                text=list(strata.values()), textposition="outside",
            ))
            fig_strata.update_layout(
                height=220, margin=dict(l=10, r=10, t=10, b=10),
                xaxis_title="Stratum", yaxis_title="Plant Count",
                template="plotly_white",
            )
            st.plotly_chart(fig_strata, use_container_width=True)
        else:
            st.info("No strata data available")

        st.markdown("### Network Health Parameters")
        craft = metrics.crafting_parameters
        peaie = metrics.peaie_parameters
        sscne = metrics.sscne_parameters

        net_tab1, net_tab2, net_tab3 = st.tabs(["CRAFTDCCV", "PEAIE", "SSCNE"])

        with net_tab1:
            if craft:
                for k, v in craft.items():
                    st.progress(v, text=f"**{k.replace('_', ' ').title()}**: {v:.2f}")
            else:
                st.caption("Loading...")

        with net_tab2:
            if peaie:
                for k, v in peaie.items():
                    st.progress(v, text=f"**{k.replace('_', ' ').title()}**: {v:.2f}")
            else:
                st.caption("Loading...")

        with net_tab3:
            if sscne:
                for k, v in sscne.items():
                    st.progress(v, text=f"**{k.replace('_', ' ').title()}**: {v:.2f}")
            else:
                st.caption("Loading...")

    if metrics.monthly_biomass_history:
        st.markdown("### Metabolic Health Trend")
        months = [h["month"] for h in metrics.monthly_biomass_history]
        ratios = [h["surplus_ratio"] for h in metrics.monthly_biomass_history]
        colors = [
            "#059669" if h["health"] == "REGENERATIVE"
            else "#2563eb" if h["health"] == "SUSTAINABLE"
            else "#d97706" if h["health"] == "STRAINED"
            else "#dc2626" if h["health"] == "MINING"
            else "#6b7280"
            for h in metrics.monthly_biomass_history
        ]
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=months, y=ratios, mode="lines+markers", name="Surplus Ratio",
            line=dict(color="#2d6a4f", width=2),
            marker=dict(size=8, color=colors),
        ))
        fig_trend.add_hline(y=1.2, line_dash="dash", line_color="#059669",
                            annotation_text="REGENERATIVE threshold (1.2)")
        fig_trend.add_hline(y=1.0, line_dash="dash", line_color="#2563eb",
                            annotation_text="SUSTAINABLE threshold (1.0)")
        fig_trend.add_hline(y=0.8, line_dash="dash", line_color="#d97706",
                            annotation_text="STRAINED threshold (0.8)")
        fig_trend.update_layout(
            height=300, template="plotly_white",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Month", yaxis_title="Surplus Ratio",
        )
        st.plotly_chart(fig_trend, use_container_width=True)


def kpi_card(label: str, value: str, unit: str, color: str):
    st.markdown(
        f"""
        <div class="kpi-card" style="border-left: 3px solid {color};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color:{color};">{value}</div>
            <div class="kpi-unit">{unit}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
