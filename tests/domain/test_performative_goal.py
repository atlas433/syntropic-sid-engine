import pytest
from decimal import Decimal
from domain.entities.performative_goal import PerformativeGoal, KPI
from domain.entities.enums import Dimension


@pytest.fixture
def sample_goal():
    return PerformativeGoal(
        id="PG-001",
        name="Closed-loop biomass cycling",
        dimension=Dimension.ECOLOGICAL,
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
    )


class TestPerformativeGoal:
    def test_create_goal(self, sample_goal):
        assert sample_goal.name == "Closed-loop biomass cycling"
        assert sample_goal.dimension == Dimension.ECOLOGICAL
        assert len(sample_goal.stakeholders) == 3
        assert len(sample_goal.kpis) == 2

    def test_is_high_priority(self, sample_goal):
        assert sample_goal.is_high_priority()

    def test_is_not_high_priority(self):
        goal = PerformativeGoal(
            id="PG-002",
            name="Low priority goal",
            dimension=Dimension.ECONOMIC,
            description="Test",
            priority=Decimal("0.5"),
        )
        assert not goal.is_high_priority()

    def test_has_kpi(self, sample_goal):
        assert sample_goal.has_kpi("Biomass surplus ratio")
        assert sample_goal.has_kpi("External fertilizer input")
        assert not sample_goal.has_kpi("Nonexistent KPI")

    def test_defaults(self):
        goal = PerformativeGoal(
            id="PG-003",
            name="Test",
            dimension=Dimension.SOCIAL,
            description="Test description",
        )
        assert goal.stakeholders == []
        assert goal.kpis == []
        assert goal.time_horizon_years == Decimal("5")
        assert goal.priority == Decimal("1.0")
        assert goal.parent_goal_id is None
