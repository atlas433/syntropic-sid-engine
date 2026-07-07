import streamlit as st
from decimal import Decimal

try:
    import pyvista as pv
    pv.OFF_SCREEN = True
except ImportError:
    pass

st.set_page_config(
    page_title="4D Ecosystem Simulator",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from interfaces.streamlit.components.styles import CSS
from interfaces.streamlit.tabs.dashboard import render_dashboard
from interfaces.streamlit.tabs.layout_2d import render_layout_2d
from interfaces.streamlit.tabs.strata_3d import render_strata_3d
from interfaces.streamlit.tabs.metabolism import render_metabolism

from infrastructure.repositories.in_memory import (
    InMemoryPlantRepository, InMemoryRowRepository,
    InMemoryGoalRepository, InMemorySystemMapRepository,
    InMemoryRoadmapRepository, InMemoryCycleRepository,
)
from application.mock_data import (
    build_species_catalog, build_mock_system,
    build_mock_goals, build_mock_system_map,
    build_mock_roadmap, build_mock_cycle,
    build_network_parameters, build_health_indicators,
)
from application.use_cases.dashboard_use_case import (
    DashboardUseCase, LayoutUseCase, SimulationUseCase,
)


def init_session_state():
    if "initialized" not in st.session_state:
        catalog, rows, plants = build_mock_system()

        plant_repo = InMemoryPlantRepository()
        row_repo = InMemoryRowRepository()
        for plant in plants:
            plant_repo.save(plant)
        for row in rows:
            row_repo.save(row)

        goals = build_mock_goals()
        goal_repo = InMemoryGoalRepository()
        for g in goals:
            goal_repo.save(g)

        system_map = build_mock_system_map()
        map_repo = InMemorySystemMapRepository()
        map_repo.save_map(system_map)
        for node in system_map.nodes:
            map_repo.save_node(node)
        for edge in system_map.edges:
            map_repo.save_edge(edge)

        roadmap = build_mock_roadmap()
        roadmap_repo = InMemoryRoadmapRepository()
        roadmap_repo.save(roadmap)

        cycle = build_mock_cycle(goals, system_map, roadmap)
        cycle_repo = InMemoryCycleRepository()
        cycle_repo.save(cycle)

        network_params = build_network_parameters()
        health_indicators = build_health_indicators()

        simulation_use_case = SimulationUseCase(
            plant_repo=plant_repo, row_repo=row_repo,
        )
        simulation_data = simulation_use_case.simulate(months=12)

        st.session_state.plant_repo = plant_repo
        st.session_state.row_repo = row_repo
        st.session_state.goal_repo = goal_repo
        st.session_state.map_repo = map_repo
        st.session_state.roadmap_repo = roadmap_repo
        st.session_state.cycle_repo = cycle_repo
        st.session_state.species_catalog = catalog
        st.session_state.goals = goals
        st.session_state.system_map = system_map
        st.session_state.roadmap = roadmap
        st.session_state.cycle = cycle
        st.session_state.network_params = network_params
        st.session_state.health_indicators = health_indicators
        st.session_state.current_month = 0
        st.session_state.simulation_data = simulation_data
        st.session_state.initialized = True


def main():
    st.markdown(CSS, unsafe_allow_html=True)

    col_title, col_month = st.columns([4, 1])
    with col_title:
        st.markdown('<div class="main-header">🌿 4D Ecosystem Simulator</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Syntropic Agroforestry × SiD Framework — Regenerative Design Engine</div>', unsafe_allow_html=True)

    with col_month:
        current = st.session_state.get("current_month", 0)
        new_month = st.number_input("Simulation Month", min_value=0, max_value=120, value=current, step=1)
        if new_month != current:
            st.session_state.current_month = new_month
            sim_uc = SimulationUseCase(
                plant_repo=st.session_state.plant_repo,
                row_repo=st.session_state.row_repo,
            )
            st.session_state.simulation_data = sim_uc.simulate(months=new_month + 1)
            st.rerun()

    dashboard_uc = DashboardUseCase(
        plant_repo=st.session_state.plant_repo,
        row_repo=st.session_state.row_repo,
    )
    layout_uc = LayoutUseCase(row_repo=st.session_state.row_repo)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard",
        "🗺️ 2D Layout",
        "🏔️ 3D Strata",
        "🔄 Metabolism",
    ])

    with tab1:
        metrics = dashboard_uc.build_metrics(
            current_month=st.session_state.current_month,
            species_catalog=st.session_state.species_catalog,
            goals=st.session_state.goals,
            network_params=st.session_state.network_params,
            health_indicators=st.session_state.health_indicators,
        )
        render_dashboard(
            metrics,
            network_params={},
            current_month=st.session_state.current_month,
        )

    with tab2:
        layout = layout_uc.build_layout()
        render_layout_2d(layout)

    with tab3:
        layout = layout_uc.build_layout()
        render_strata_3d(layout)

    with tab4:
        sim_data = st.session_state.get("simulation_data", [])
        render_metabolism(sim_data)


if __name__ == "__main__":
    init_session_state()
    main()
