import pytest
from decimal import Decimal
from domain.entities.cycle import SiDCycle, EvaluationResult, FIBONACCI_CYCLE_DURATIONS
from domain.entities.performative_goal import PerformativeGoal
from domain.entities.enums import SnoLevel, ELSICategory


class TestEvaluationResult:
    def test_create_evaluation(self):
        result = EvaluationResult(
            goals_achieved=True,
            unintended_consequences=["Slight runoff increase in wet season"],
            needs_another_cycle=False,
            notes="All targets met. Ready for implementation.",
        )
        assert result.goals_achieved
        assert len(result.unintended_consequences) == 1
        assert not result.needs_another_cycle

    def test_defaults(self):
        result = EvaluationResult(goals_achieved=False)
        assert result.unintended_consequences == []
        assert result.needs_another_cycle
        assert result.notes == ""


class TestSiDCycle:
    def test_create_cycle(self):
        cycle = SiDCycle(
            cycle_number=1,
            days=1,
            purpose="Reconnaissance — quick survey of entire challenge",
        )
        assert cycle.cycle_number == 1
        assert cycle.days == 1
        assert cycle.is_reconnaissance
        assert not cycle.is_deep_analysis
        assert cycle.goals == []
        assert cycle.system_maps == []

    def test_is_reconnaissance(self):
        cycle1 = SiDCycle(cycle_number=1, days=1)
        cycle2 = SiDCycle(cycle_number=2, days=1)
        cycle3 = SiDCycle(cycle_number=3, days=2)
        assert cycle1.is_reconnaissance
        assert cycle2.is_reconnaissance
        assert not cycle3.is_reconnaissance

    def test_is_deep_analysis(self):
        cycle3 = SiDCycle(cycle_number=3, days=2)
        cycle4 = SiDCycle(cycle_number=4, days=3)
        cycle6 = SiDCycle(cycle_number=6, days=8)
        assert not cycle3.is_deep_analysis
        assert cycle4.is_deep_analysis
        assert cycle6.is_deep_analysis

    def test_evaluate(self):
        cycle = SiDCycle(cycle_number=3, days=2)
        assert cycle.evaluation is None

        cycle.evaluate(
            goals_achieved=True,
            notes="Maps look solid. Ready for solutioning.",
            unintended_consequences=["Minor stakeholder tension identified"],
            needs_another_cycle=True,
        )
        assert cycle.evaluation is not None
        assert cycle.evaluation.goals_achieved
        assert len(cycle.evaluation.unintended_consequences) == 1

    def test_with_goals(self):
        goal = PerformativeGoal(
            id="PG-001",
            name="Closed-loop biomass",
            level=SnoLevel.SYSTEM,
            elsi_category=ELSICategory.ECOSYSTEMS,
            description="Test goal",
        )
        cycle = SiDCycle(
            cycle_number=4,
            days=3,
            goals=[goal],
        )
        assert len(cycle.goals) == 1
        assert cycle.goals[0].name == "Closed-loop biomass"


class TestFibonacciDurations:
    def test_all_8_cycles(self):
        assert len(FIBONACCI_CYCLE_DURATIONS) == 8

    def test_fibonacci_values(self):
        assert FIBONACCI_CYCLE_DURATIONS[1] == 1
        assert FIBONACCI_CYCLE_DURATIONS[2] == 1
        assert FIBONACCI_CYCLE_DURATIONS[3] == 2
        assert FIBONACCI_CYCLE_DURATIONS[4] == 3
        assert FIBONACCI_CYCLE_DURATIONS[5] == 5
        assert FIBONACCI_CYCLE_DURATIONS[6] == 8
        assert FIBONACCI_CYCLE_DURATIONS[7] == 13
        assert FIBONACCI_CYCLE_DURATIONS[8] == 21
