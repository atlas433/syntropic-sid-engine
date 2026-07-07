import pytest
from decimal import Decimal
from domain.entities.performative_goal import PerformativeGoal, KPI
from domain.entities.enums import SnoLevel, ELSICategory


@pytest.fixture
def sample_goal():
    return PerformativeGoal(
        id="PG-001",
        name="Closed-loop biomass cycling",
        level=SnoLevel.SYSTEM,
        elsi_category=ELSICategory.ECOSYSTEMS,
        description="The agroforestry system maintains soil fertility entirely through internal biomass production.",
        stakeholders=["Farm operators", "Soil microbiome", "Downstream water users"],
        kpis=[
            KPI(name="Biomass surplus ratio", unit="ratio", target="> 1.2"),
            KPI(name="External fertilizer input", unit="kg/ha/year", target="= 0"),
        ],
        time_horizon_years=Decimal("5"),
        priority=Decimal("1.0"),
        conflicting_goals=[],
        synergistic_goals=["PG-003", "PG-007"],
        system_boundary="The 10-hectare farm plot and adjacent water catchments",
        vision="A self-sustaining forest ecosystem that also feeds the community",
    )


class TestPerformativeGoal:
    def test_create_goal(self, sample_goal):
        assert sample_goal.name == "Closed-loop biomass cycling"
        assert sample_goal.level == SnoLevel.SYSTEM
        assert sample_goal.elsi_category == ELSICategory.ECOSYSTEMS
        assert len(sample_goal.stakeholders) == 3
        assert len(sample_goal.kpis) == 2

    def test_is_high_priority(self, sample_goal):
        assert sample_goal.is_high_priority()

    def test_is_not_high_priority(self):
        goal = PerformativeGoal(
            id="PG-002",
            name="Low priority goal",
            level=SnoLevel.OBJECT,
            elsi_category=ELSICategory.ECONOMY,
            description="Test",
            priority=Decimal("0.5"),
        )
        assert not goal.is_high_priority()

    def test_is_system_level(self, sample_goal):
        assert sample_goal.is_system_level()

    def test_is_not_system_level(self):
        goal = PerformativeGoal(
            id="PG-004",
            name="Object level",
            level=SnoLevel.OBJECT,
            elsi_category=ELSICategory.ENERGY,
            description="Test",
        )
        assert not goal.is_system_level()

    def test_has_kpi(self, sample_goal):
        assert sample_goal.has_kpi("Biomass surplus ratio")
        assert sample_goal.has_kpi("External fertilizer input")
        assert not sample_goal.has_kpi("Nonexistent KPI")

    def test_defaults(self):
        goal = PerformativeGoal(
            id="PG-003",
            name="Test",
            level=SnoLevel.NETWORK,
            elsi_category=ELSICategory.MATERIALS,
            description="Test description",
        )
        assert goal.stakeholders == []
        assert goal.kpis == []
        assert goal.time_horizon_years == Decimal("5")
        assert goal.priority == Decimal("1.0")
        assert goal.parent_goal_id is None
        assert goal.system_boundary == ""
        assert goal.vision == ""
        assert goal.project_boundaries == {}

    def test_elsi_category_range(self):
        goal = PerformativeGoal(
            id="PG-005",
            name="Energy goal",
            level=SnoLevel.SYSTEM,
            elsi_category=ELSICategory.ENERGY,
            description="Test",
        )
        assert goal.elsi_category == ELSICategory.ENERGY

    def test_all_elsi_categories(self):
        assert len(ELSICategory) == 8
        categories = {c for c in ELSICategory}
        assert ELSICategory.HEALTH in categories
        assert ELSICategory.HAPPINESS in categories
