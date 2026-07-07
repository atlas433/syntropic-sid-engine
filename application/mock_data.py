from decimal import Decimal
from uuid import uuid4

from domain.entities.enums import (
    Stratum,
    SuccessionStage,
    LightRequirement,
    RowType,
    WaterRequirement,
    PruningRegime,
    SnoLevel,
    ELSICategory,
    MapDimension,
    MapScale,
    NodeType,
    EdgeType,
    Nonlinearity,
    Boundary,
    TransitionType,
    ActionType,
)
from domain.entities.species import SpeciesDefinition
from domain.entities.plant import Plant
from domain.entities.row import Row
from domain.entities.system_map import SystemNode, SystemEdge, SystemMap
from domain.entities.performative_goal import PerformativeGoal, KPI
from domain.entities.roadmap import (
    Intervention, DecisionPoint, Risk, TransitionPhase,
    SolutionChannel, Governance, TransitionRoadmap,
)
from domain.entities.cycle import SiDCycle, FIBONACCI_CYCLE_DURATIONS
from domain.value_objects.indicators import (
    HealthIndicators, CraftdccvParameters, PeaieParameters,
    SscneParameters, NetworkParameters,
)


def build_species_catalog() -> list[SpeciesDefinition]:
    return [
        SpeciesDefinition(
            id="SP-001", common_name="Pigeon Pea", scientific_name="Cajanus cajan",
            stratum=Stratum.MEDIUM, successional_stage=SuccessionStage.PLACENTA,
            lifecycle_years=Decimal("3"), growth_rate_cm_per_year=Decimal("200"),
            mature_height_m=Decimal("3"), canopy_diameter_m=Decimal("2"),
            biomass_production_kg_m_year=Decimal("4.5"), nitrogen_fixation=True,
            light_requirement=LightRequirement.HELIOPHILE, water_requirement=WaterRequirement.MEDIUM,
            mulch_quality_cn_ratio=Decimal("15"), harvestable_yield="pods, green manure",
            row_type=RowType.A, pruning_regime=PruningRegime.AGGRESSIVE, pruning_interval_months=3,
        ),
        SpeciesDefinition(
            id="SP-002", common_name="Leucaena", scientific_name="Leucaena leucocephala",
            stratum=Stratum.HIGH, successional_stage=SuccessionStage.PLACENTA,
            lifecycle_years=Decimal("5"), growth_rate_cm_per_year=Decimal("300"),
            mature_height_m=Decimal("6"), canopy_diameter_m=Decimal("3"),
            biomass_production_kg_m_year=Decimal("6.0"), nitrogen_fixation=True,
            light_requirement=LightRequirement.HELIOPHILE, water_requirement=WaterRequirement.LOW,
            mulch_quality_cn_ratio=Decimal("12"), harvestable_yield="leaf biomass, fodder",
            row_type=RowType.A, pruning_regime=PruningRegime.AGGRESSIVE, pruning_interval_months=3,
        ),
        SpeciesDefinition(
            id="SP-003", common_name="Banana", scientific_name="Musa paradisiaca",
            stratum=Stratum.MEDIUM, successional_stage=SuccessionStage.SECONDARY_I,
            lifecycle_years=Decimal("6"), growth_rate_cm_per_year=Decimal("150"),
            mature_height_m=Decimal("4"), canopy_diameter_m=Decimal("3"),
            biomass_production_kg_m_year=Decimal("10.0"), nitrogen_fixation=False,
            light_requirement=LightRequirement.INTERMEDIATE, water_requirement=WaterRequirement.HIGH,
            mulch_quality_cn_ratio=Decimal("25"), harvestable_yield="fruit, pseudostem biomass",
            row_type=RowType.C, pruning_regime=PruningRegime.SELECTIVE, pruning_interval_months=6,
        ),
        SpeciesDefinition(
            id="SP-004", common_name="Cassava", scientific_name="Manihot esculenta",
            stratum=Stratum.LOW, successional_stage=SuccessionStage.PLACENTA,
            lifecycle_years=Decimal("2"), growth_rate_cm_per_year=Decimal("120"),
            mature_height_m=Decimal("2"), canopy_diameter_m=Decimal("1.5"),
            biomass_production_kg_m_year=Decimal("3.0"), nitrogen_fixation=False,
            light_requirement=LightRequirement.INTERMEDIATE, water_requirement=WaterRequirement.LOW,
            mulch_quality_cn_ratio=Decimal("20"), harvestable_yield="tubers, leaf",
            row_type=RowType.C, pruning_regime=PruningRegime.FORMATIVE, pruning_interval_months=12,
        ),
        SpeciesDefinition(
            id="SP-005", common_name="Avocado", scientific_name="Persea americana",
            stratum=Stratum.HIGH, successional_stage=SuccessionStage.SECONDARY_II,
            lifecycle_years=Decimal("40"), growth_rate_cm_per_year=Decimal("60"),
            mature_height_m=Decimal("10"), canopy_diameter_m=Decimal("8"),
            biomass_production_kg_m_year=Decimal("8.0"), nitrogen_fixation=False,
            light_requirement=LightRequirement.HELIOPHILE, water_requirement=WaterRequirement.HIGH,
            mulch_quality_cn_ratio=Decimal("40"), harvestable_yield="fruit",
            row_type=RowType.C, pruning_regime=PruningRegime.FORMATIVE, pruning_interval_months=12,
        ),
        SpeciesDefinition(
            id="SP-006", common_name="Mahogany", scientific_name="Swietenia macrophylla",
            stratum=Stratum.EMERGENT, successional_stage=SuccessionStage.PRIMARY,
            lifecycle_years=Decimal("200"), growth_rate_cm_per_year=Decimal("40"),
            mature_height_m=Decimal("30"), canopy_diameter_m=Decimal("15"),
            biomass_production_kg_m_year=Decimal("20.0"), nitrogen_fixation=False,
            light_requirement=LightRequirement.HELIOPHILE, water_requirement=WaterRequirement.MEDIUM,
            mulch_quality_cn_ratio=Decimal("80"), harvestable_yield="timber",
            row_type=RowType.C, pruning_regime=PruningRegime.NONE, pruning_interval_months=0,
        ),
        SpeciesDefinition(
            id="SP-007", common_name="Sweet Potato", scientific_name="Ipomoea batatas",
            stratum=Stratum.GROUND_COVER, successional_stage=SuccessionStage.PLACENTA,
            lifecycle_years=Decimal("1"), growth_rate_cm_per_year=Decimal("80"),
            mature_height_m=Decimal("0.3"), canopy_diameter_m=Decimal("1.5"),
            biomass_production_kg_m_year=Decimal("2.0"), nitrogen_fixation=False,
            light_requirement=LightRequirement.INTERMEDIATE, water_requirement=WaterRequirement.MEDIUM,
            mulch_quality_cn_ratio=Decimal("18"), harvestable_yield="tubers, leaf greens",
            row_type=RowType.C, pruning_regime=PruningRegime.NONE, pruning_interval_months=0,
        ),
        SpeciesDefinition(
            id="SP-008", common_name="Coffee", scientific_name="Coffea arabica",
            stratum=Stratum.MEDIUM, successional_stage=SuccessionStage.SECONDARY_II,
            lifecycle_years=Decimal("25"), growth_rate_cm_per_year=Decimal("30"),
            mature_height_m=Decimal("3"), canopy_diameter_m=Decimal("2.5"),
            biomass_production_kg_m_year=Decimal("2.5"), nitrogen_fixation=False,
            light_requirement=LightRequirement.SCIOPHYTE, water_requirement=WaterRequirement.MEDIUM,
            mulch_quality_cn_ratio=Decimal("22"), harvestable_yield="coffee cherries",
            row_type=RowType.C, pruning_regime=PruningRegime.SELECTIVE, pruning_interval_months=12,
        ),
        SpeciesDefinition(
            id="SP-009", common_name="Eucalyptus", scientific_name="Eucalyptus grandis",
            stratum=Stratum.EMERGENT, successional_stage=SuccessionStage.SECONDARY_I,
            lifecycle_years=Decimal("60"), growth_rate_cm_per_year=Decimal("250"),
            mature_height_m=Decimal("35"), canopy_diameter_m=Decimal("10"),
            biomass_production_kg_m_year=Decimal("15.0"), nitrogen_fixation=False,
            light_requirement=LightRequirement.HELIOPHILE, water_requirement=WaterRequirement.HIGH,
            mulch_quality_cn_ratio=Decimal("60"), harvestable_yield="timber, poles, biomass",
            row_type=RowType.A, pruning_regime=PruningRegime.SELECTIVE, pruning_interval_months=6,
        ),
        SpeciesDefinition(
            id="SP-010", common_name="Inga", scientific_name="Inga edulis",
            stratum=Stratum.HIGH, successional_stage=SuccessionStage.SECONDARY_I,
            lifecycle_years=Decimal("15"), growth_rate_cm_per_year=Decimal("180"),
            mature_height_m=Decimal("8"), canopy_diameter_m=Decimal("6"),
            biomass_production_kg_m_year=Decimal("7.0"), nitrogen_fixation=True,
            light_requirement=LightRequirement.HELIOPHILE, water_requirement=WaterRequirement.MEDIUM,
            mulch_quality_cn_ratio=Decimal("14"), harvestable_yield="fruit pulp, shade, biomass",
            row_type=RowType.A, pruning_regime=PruningRegime.AGGRESSIVE, pruning_interval_months=6,
        ),
        SpeciesDefinition(
            id="SP-011", common_name="Cacao", scientific_name="Theobroma cacao",
            stratum=Stratum.LOW, successional_stage=SuccessionStage.SECONDARY_II,
            lifecycle_years=Decimal("30"), growth_rate_cm_per_year=Decimal("40"),
            mature_height_m=Decimal("5"), canopy_diameter_m=Decimal("3"),
            biomass_production_kg_m_year=Decimal("3.5"), nitrogen_fixation=False,
            light_requirement=LightRequirement.SCIOPHYTE, water_requirement=WaterRequirement.HIGH,
            mulch_quality_cn_ratio=Decimal("20"), harvestable_yield="cacao pods",
            row_type=RowType.C, pruning_regime=PruningRegime.FORMATIVE, pruning_interval_months=12,
        ),
        SpeciesDefinition(
            id="SP-012", common_name="Jackfruit", scientific_name="Artocarpus heterophyllus",
            stratum=Stratum.EMERGENT, successional_stage=SuccessionStage.PRIMARY,
            lifecycle_years=Decimal("80"), growth_rate_cm_per_year=Decimal("100"),
            mature_height_m=Decimal("20"), canopy_diameter_m=Decimal("12"),
            biomass_production_kg_m_year=Decimal("12.0"), nitrogen_fixation=False,
            light_requirement=LightRequirement.HELIOPHILE, water_requirement=WaterRequirement.MEDIUM,
            mulch_quality_cn_ratio=Decimal("50"), harvestable_yield="fruit, timber",
            row_type=RowType.C, pruning_regime=PruningRegime.FORMATIVE, pruning_interval_months=12,
        ),
    ]


def build_mock_system():
    catalog = build_species_catalog()
    species_map = {s.id: s for s in catalog}
    rows: list[Row] = []
    plants: list[Plant] = []
    month = 12

    a_row_1 = Row(id="A-1", row_type=RowType.A, length_m=Decimal("100"),
                   soil_organic_matter_kg_per_m=Decimal("6.2"))
    a_row_2 = Row(id="A-2", row_type=RowType.A, length_m=Decimal("100"),
                   soil_organic_matter_kg_per_m=Decimal("5.8"))

    for i in range(60):
        sp = species_map["SP-001"] if i < 30 else species_map["SP-002"]
        plant = Plant(id=uuid4(), species=sp, age_months=month, current_height_m=Decimal("1.5") + Decimal(i % 5) * Decimal("0.2"))
        a_row_1.add_plant(plant)
        plants.append(plant)
    for i in range(25):
        sp = species_map["SP-010"] if i < 15 else species_map["SP-009"]
        plant = Plant(id=uuid4(), species=sp, age_months=month, current_height_m=Decimal("2.0") + Decimal(i % 3) * Decimal("0.3"))
        a_row_2.add_plant(plant)
        plants.append(plant)

    rows.append(a_row_1)
    rows.append(a_row_2)

    c_row_1 = Row(id="C-1", row_type=RowType.C, length_m=Decimal("100"))
    c_row_2 = Row(id="C-2", row_type=RowType.C, length_m=Decimal("100"))
    c_row_3 = Row(id="C-3", row_type=RowType.C, length_m=Decimal("100"))

    c1_assignments = [
        ("SP-005", 0, 8), ("SP-005", 1, 12), ("SP-005", 2, 20),
        ("SP-008", 3, 10), ("SP-008", 4, 15), ("SP-008", 5, 25),
        ("SP-006", 6, 24), ("SP-011", 7, 6),
    ]
    for sp_id, idx, age in c1_assignments:
        plant = Plant(id=uuid4(), species=species_map[sp_id], age_months=month + age,
                       current_height_m=Decimal("0.8") + Decimal(idx) * Decimal("0.3"))
        c_row_1.add_plant(plant)
        plants.append(plant)

    c2_assignments = [
        ("SP-003", 0, 10), ("SP-003", 1, 15), ("SP-003", 2, 20),
        ("SP-004", 3, 8), ("SP-004", 4, 12), ("SP-004", 5, 18),
        ("SP-012", 6, 36), ("SP-007", 7, 3), ("SP-007", 8, 3),
    ]
    for sp_id, idx, age in c2_assignments:
        plant = Plant(id=uuid4(), species=species_map[sp_id], age_months=month + age,
                       current_height_m=Decimal("1.0") + Decimal(idx) * Decimal("0.25"))
        c_row_2.add_plant(plant)
        plants.append(plant)

    c3_assignments = [
        ("SP-005", 0, 6), ("SP-005", 1, 14), ("SP-003", 2, 18),
        ("SP-008", 3, 22), ("SP-011", 4, 8), ("SP-011", 5, 12),
        ("SP-006", 6, 48), ("SP-007", 7, 2),
    ]
    for sp_id, idx, age in c3_assignments:
        plant = Plant(id=uuid4(), species=species_map[sp_id], age_months=month + age,
                       current_height_m=Decimal("0.6") + Decimal(idx) * Decimal("0.35"))
        c_row_3.add_plant(plant)
        plants.append(plant)

    rows.append(c_row_1)
    rows.append(c_row_2)
    rows.append(c_row_3)

    return catalog, rows, plants


def build_mock_goals() -> list[PerformativeGoal]:
    return [
        PerformativeGoal(
            id="PG-001", name="Closed-loop biomass cycling",
            level=SnoLevel.SYSTEM, elsi_category=ELSICategory.ECOSYSTEMS,
            description="The agroforestry system maintains soil fertility entirely through internal biomass production, eliminating external fertilizer inputs.",
            stakeholders=["Farm operators", "Soil microbiome", "Downstream water users"],
            kpis=[KPI(name="Biomass surplus ratio", unit="ratio", target="> 1.2"),
                  KPI(name="External fertilizer input", unit="kg/ha/year", target="= 0")],
            time_horizon_years=Decimal("5"), priority=Decimal("1.0"),
        ),
        PerformativeGoal(
            id="PG-002", name="Complete strata occupation",
            level=SnoLevel.NETWORK, elsi_category=ELSICategory.SPECIES,
            description="All five vertical strata are occupied by productive species across the entire field, maximizing photosynthetic capture.",
            stakeholders=["Farm operators", "Local biodiversity"],
            kpis=[KPI(name="Strata occupation rate", unit="ratio", target="= 1.0"),
                  KPI(name="Species count per stratum", unit="count", target=">= 3")],
            time_horizon_years=Decimal("3"), priority=Decimal("0.9"),
        ),
        PerformativeGoal(
            id="PG-003", name="Energy positive operations",
            level=SnoLevel.OBJECT, elsi_category=ELSICategory.ENERGY,
            description="The system generates more renewable energy than it consumes for farm operations.",
            stakeholders=["Farm operators", "Local grid"],
            kpis=[KPI(name="Energy surplus", unit="MWh/year", target="> 0")],
            time_horizon_years=Decimal("2"), priority=Decimal("0.7"),
        ),
        PerformativeGoal(
            id="PG-004", name="Economic viability",
            level=SnoLevel.SYSTEM, elsi_category=ELSICategory.ECONOMY,
            description="The agroforestry system generates sufficient revenue to support farm operations and provide living wages.",
            stakeholders=["Farm operators", "Workers", "Local economy"],
            kpis=[KPI(name="Annual revenue", unit="USD", target="> 50000"),
                  KPI(name="ROI", unit="percent", target="> 15")],
            time_horizon_years=Decimal("5"), priority=Decimal("0.85"),
        ),
        PerformativeGoal(
            id="PG-005", name="Biodiversity enhancement",
            level=SnoLevel.NETWORK, elsi_category=ELSICategory.SPECIES,
            description="The system supports increasing biodiversity of both planted and spontaneous species.",
            stakeholders=["Local ecosystem", "Conservation groups"],
            kpis=[KPI(name="Shannon diversity index", unit="index", target="> 2.5"),
                  KPI(name="Bird species count", unit="count", target="> 20")],
            time_horizon_years=Decimal("5"), priority=Decimal("0.8"),
        ),
    ]


def build_mock_system_map() -> SystemMap:
    sm = SystemMap(id="SM-001", name="Agroforestry Metabolic System",
                   map_dimension=MapDimension.CONTEXT, map_scale=MapScale.MEDIUM)
    nodes = [
        SystemNode(id="N-001", name="A-Row Biomass", node_type=NodeType.STOCK,
                   elsi_category=ELSICategory.MATERIALS, scope=SnoLevel.OBJECT,
                   boundary=Boundary.INTERNAL, initial_value=Decimal("500"), unit="kg"),
        SystemNode(id="N-002", name="Soil Organic Matter", node_type=NodeType.STOCK,
                   elsi_category=ELSICategory.ECOSYSTEMS, scope=SnoLevel.OBJECT,
                   boundary=Boundary.INTERNAL, initial_value=Decimal("6000"), unit="kg"),
        SystemNode(id="N-003", name="C-Row Nutrient Demand", node_type=NodeType.FLOW,
                   elsi_category=ELSICategory.MATERIALS, scope=SnoLevel.OBJECT,
                   boundary=Boundary.INTERNAL, initial_value=Decimal("400"), unit="kg/month"),
        SystemNode(id="N-004", name="Sunlight Capture", node_type=NodeType.FLOW,
                   elsi_category=ELSICategory.ENERGY, scope=SnoLevel.OBJECT,
                   boundary=Boundary.EXTERNAL, initial_value=Decimal("2000"), unit="kWh/m²/year"),
        SystemNode(id="N-005", name="Soil Microbiome", node_type=NodeType.ACTOR,
                   elsi_category=ELSICategory.ECOSYSTEMS, scope=SnoLevel.NETWORK,
                   boundary=Boundary.INTERNAL),
        SystemNode(id="N-006", name="Farm Operator", node_type=NodeType.ACTOR,
                   elsi_category=ELSICategory.CULTURE, scope=SnoLevel.NETWORK,
                   boundary=Boundary.INTERNAL),
        SystemNode(id="N-007", name="Pruning Events", node_type=NodeType.LEVERAGE_POINT,
                   elsi_category=ELSICategory.MATERIALS, scope=SnoLevel.OBJECT,
                   boundary=Boundary.INTERNAL),
        SystemNode(id="N-008", name="Rainfall", node_type=NodeType.EXTERNALITY,
                   elsi_category=ELSICategory.ENERGY, scope=SnoLevel.OBJECT,
                   boundary=Boundary.EXTERNAL, initial_value=Decimal("1200"), unit="mm/year"),
    ]
    edges = [
        SystemEdge(id="E-001", source_node_id="N-001", target_node_id="N-003",
                   edge_type=EdgeType.MATERIAL_FLOW, strength=Decimal("0.85"),
                   delay_months=1, nonlinearity=Nonlinearity.DIMINISHING_RETURNS,
                   description="Pruned biomass decomposes and feeds C-rows"),
        SystemEdge(id="E-002", source_node_id="N-001", target_node_id="N-002",
                   edge_type=EdgeType.MATERIAL_FLOW, strength=Decimal("0.15"),
                   delay_months=3, description="Residual biomass builds soil organic matter"),
        SystemEdge(id="E-003", source_node_id="N-004", target_node_id="N-001",
                   edge_type=EdgeType.ENERGY_FLOW, strength=Decimal("0.8"),
                   description="Sunlight drives photosynthesis and biomass production"),
        SystemEdge(id="E-004", source_node_id="N-007", target_node_id="N-001",
                   edge_type=EdgeType.CAUSAL_POSITIVE, strength=Decimal("0.7"),
                   description="Pruning stimulates regrowth and biomass production"),
        SystemEdge(id="E-005", source_node_id="N-005", target_node_id="N-003",
                   edge_type=EdgeType.CAUSAL_POSITIVE, strength=Decimal("0.6"),
                   delay_months=2, description="Microbiome mineralizes biomass for plant uptake"),
        SystemEdge(id="E-006", source_node_id="N-002", target_node_id="N-005",
                   edge_type=EdgeType.CAUSAL_POSITIVE, strength=Decimal("0.5"),
                   description="Soil organic matter supports microbial communities"),
        SystemEdge(id="E-007", source_node_id="N-006", target_node_id="N-007",
                   edge_type=EdgeType.REGULATORY, strength=Decimal("0.9"),
                   description="Farmer decides pruning schedule and intensity"),
        SystemEdge(id="E-008", source_node_id="N-003", target_node_id="N-002",
                   edge_type=EdgeType.CAUSAL_NEGATIVE, strength=Decimal("-0.4"),
                   description="Excess nutrient demand depletes soil organic matter"),
        SystemEdge(id="E-009", source_node_id="N-008", target_node_id="N-001",
                   edge_type=EdgeType.CAUSAL_POSITIVE, strength=Decimal("0.5"),
                   description="Rainfall supports plant growth"),
    ]
    for n in nodes:
        sm.add_node(n)
    for e in edges:
        sm.add_edge(e)
    return sm


def build_mock_roadmap() -> TransitionRoadmap:
    roadmap = TransitionRoadmap(id="RM-001", name="Syntropic Farm Establishment",
                                 time_horizon_years=Decimal("5"))
    chan = SolutionChannel(id="SC-001", name="Field Operations")
    chan.add_phase(TransitionPhase(
        id="PH-01", name="Soil Prep & Placenta", duration_months=6,
        transition_type=TransitionType.START,
        interventions=[
            Intervention(id="INT-001", name="Plant pioneer A-rows",
                         description="Establish dense A-row planting with Pigeon Pea and Leucaena at 0.5m spacing",
                         affected_nodes=["N-001", "N-007"], action_type=ActionType.SYSTEMIC,
                         expected_impact=Decimal("0.8"), trigger_conditions="month == 0",
                         cost=Decimal("3000"), duration_months=2),
            Intervention(id="INT-002", name="Establish ground cover",
                         description="Plant Sweet Potato as living mulch across all C-rows",
                         affected_nodes=["N-002", "N-003"], action_type=ActionType.PULL,
                         expected_impact=Decimal("0.6"), trigger_conditions="month == 0",
                         cost=Decimal("500"), duration_months=1),
        ],
        decision_points=[
            DecisionPoint(id="DP-001", month=6,
                          condition="soil_cover >= 0.8 AND soil_organic_carbon >= baseline",
                          if_true_proceed_to="PH-02", if_false_proceed_to="PH-01b"),
        ],
    ))
    chan.add_phase(TransitionPhase(
        id="PH-02", name="Secondary I Integration", duration_months=12,
        transition_type=TransitionType.CHANGE,
        interventions=[
            Intervention(id="INT-003", name="Plant fruit trees in C-rows",
                         description="Introduce Avocado, Banana, and Coffee into C-rows under established shade",
                         affected_nodes=["N-003"], action_type=ActionType.PULL,
                         expected_impact=Decimal("0.7"), trigger_conditions="month >= 6",
                         cost=Decimal("4000"), duration_months=3),
            Intervention(id="INT-004", name="Increase mulch application",
                         description="Aggressive pruning of mature A-row biomass to feed expanding C-rows",
                         affected_nodes=["N-001", "N-007"], action_type=ActionType.LUBRICATE,
                         expected_impact=Decimal("0.5"), trigger_conditions="month >= 6",
                         cost=Decimal("0"), duration_months=12),
        ],
        decision_points=[
            DecisionPoint(id="DP-002", month=18,
                          condition="biomass_surplus_ratio >= 1.2",
                          if_true_proceed_to="PH-03", if_false_proceed_to="PH-02b"),
        ],
    ))
    chan.add_phase(TransitionPhase(
        id="PH-03", name="Secondary II & Fruit Production", duration_months=24,
        transition_type=TransitionType.ENABLE,
        interventions=[
            Intervention(id="INT-005", name="Plant timber species",
                         description="Introduce Mahogany and Jackfruit at final spacing for long-term canopy",
                         affected_nodes=["N-004"], action_type=ActionType.PULL,
                         expected_impact=Decimal("0.6"), trigger_conditions="month >= 18",
                         cost=Decimal("2000"), duration_months=2),
        ],
    ))
    roadmap.solution_channels.append(chan)

    gov_chan = SolutionChannel(id="SC-002", name="Governance & Monitoring")
    gov_chan.add_phase(TransitionPhase(
        id="PH-GOV", name="Ongoing", duration_months=60,
        transition_type=TransitionType.GOVERN,
        interventions=[
            Intervention(id="INT-006", name="Monthly metabolic check",
                         description="Run metabolic service simulation and verify surplus ratio",
                         affected_nodes=[], action_type=ActionType.LUBRICATE,
                         expected_impact=Decimal("0.3"), trigger_conditions="every month",
                         cost=Decimal("200"), duration_months=1),
        ],
    ))
    roadmap.solution_channels.append(gov_chan)

    roadmap.governance = Governance(
        communication_plan="Monthly dashboard review, quarterly stakeholder meeting",
        monitoring_frequency_months=1, stakeholder_updates=["Farm team", "Investors"],
        budget_allocation=Decimal("15000"),
    )
    return roadmap


def build_mock_cycle(goals: list[PerformativeGoal], system_map: SystemMap,
                     roadmap: TransitionRoadmap) -> SiDCycle:
    duration = FIBONACCI_CYCLE_DURATIONS[3]
    cycle = SiDCycle(cycle_number=3, days=duration,
                     purpose="Deep analysis: refine system maps and develop initial solutions")
    cycle.goals = goals
    cycle.system_maps = [system_map]
    cycle.solutions = []
    for ch in roadmap.solution_channels:
        for ph in ch.phases:
            cycle.solutions.extend(ph.interventions)
    return cycle


def build_network_parameters() -> NetworkParameters:
    return NetworkParameters(
        craftdccv=CraftdccvParameters(
            connectivity=Decimal("0.65"), redundancy=Decimal("0.55"),
            awareness=Decimal("0.70"), flexibility=Decimal("0.60"),
            transparency=Decimal("0.75"), diversity=Decimal("0.80"),
            complexity=Decimal("0.50"), centrality=Decimal("0.30"),
            variety=Decimal("0.72"),
        ),
        peaie=PeaieParameters(
            productivity=Decimal("0.78"), efficiency=Decimal("0.72"),
            autonomy=Decimal("0.65"), integrity=Decimal("0.80"),
            emergence=Decimal("0.55"),
        ),
        sscne=SscneParameters(
            synergy=Decimal("0.70"), self_organization=Decimal("0.60"),
            synchronicity=Decimal("0.68"), nestedness=Decimal("0.75"),
            evolution=Decimal("0.58"),
        ),
        reinforcing_loops=3, balancing_loops=2,
    )


def build_health_indicators() -> HealthIndicators:
    return HealthIndicators(
        surplus_ratio=Decimal("1.35"), mulch_coverage_ratio=Decimal("1.10"),
        soil_carbon_trend=Decimal("0.05"), diversity_shannon_index=Decimal("2.45"),
        circularity=Decimal("0.85"), resilience_index=Decimal("0.72"),
    )
