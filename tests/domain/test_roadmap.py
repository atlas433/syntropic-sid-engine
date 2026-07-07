import pytest
from decimal import Decimal
from domain.entities.roadmap import (
    TransitionPhase, TransitionRoadmap,
    Intervention, DecisionPoint, Risk,
)


class TestIntervention:
    def test_create_intervention(self):
        iv = Intervention(
            id="INT-001",
            name="Plant pioneer A-rows",
            description="Establish dense A-row planting with fast-growing N-fixing species.",
            affected_nodes=["soil_nitrogen", "soil_cover", "biomass_standing"],
            affected_edges=["E-001"],
            expected_impact=Decimal("0.7"),
            trigger_conditions="month == 0",
            cost=Decimal("5000"),
            duration_months=2,
        )
        assert iv.name == "Plant pioneer A-rows"
        assert len(iv.affected_nodes) == 3
        assert iv.expected_impact == Decimal("0.7")

    def test_defaults(self):
        iv = Intervention(id="INT-002", name="Test", description="Test")
        assert iv.affected_nodes == []
        assert iv.affected_edges == []
        assert iv.expected_impact == Decimal("0")
        assert iv.trigger_conditions == ""
        assert iv.cost == Decimal("0")
        assert iv.duration_months == 1
        assert iv.dependencies == []


class TestDecisionPoint:
    def test_create_decision_point(self):
        dp = DecisionPoint(
            id="DP-001",
            month=6,
            condition="soil_cover >= 0.8",
            if_true_proceed_to="PH-02",
            if_false_proceed_to="PH-01b",
        )
        assert dp.month == 6
        assert dp.if_true_proceed_to == "PH-02"


class TestRisk:
    def test_risk_score(self):
        risk = Risk(
            id="R-001",
            description="Drought during establishment phase",
            probability=Decimal("0.3"),
            impact=Decimal("0.8"),
            mitigation="Install drip irrigation backup",
        )
        assert risk.risk_score == Decimal("0.24")


class TestTransitionPhase:
    def test_create_phase(self):
        phase = TransitionPhase(
            id="PH-01",
            name="Soil Preparation & Placenta Establishment",
            duration_months=6,
            interventions=[
                Intervention(id="INT-001", name="Plant pioneer A-rows",
                             description="Plant pioneer A-rows",
                             expected_impact=Decimal("0.7")),
            ],
            decision_points=[
                DecisionPoint(id="DP-001", month=6, condition="soil_cover >= 0.8",
                              if_true_proceed_to="PH-02", if_false_proceed_to="PH-01b"),
            ],
            risks=[
                Risk(id="R-001", description="Drought", probability=Decimal("0.3"),
                     impact=Decimal("0.8"), mitigation="Irrigation"),
            ],
        )
        assert len(phase.interventions) == 1
        assert len(phase.decision_points) == 1
        assert len(phase.risks) == 1


class TestTransitionRoadmap:
    def test_create_roadmap(self):
        roadmap = TransitionRoadmap(
            id="TR-001",
            name="Full Syntropic Transition",
            time_horizon_years=Decimal("10"),
            phases=[
                TransitionPhase(
                    id="PH-01",
                    name="Phase 1: Establishment",
                    duration_months=6,
                ),
                TransitionPhase(
                    id="PH-02",
                    name="Phase 2: Secondary Integration",
                    duration_months=18,
                ),
            ],
        )
        assert roadmap.total_duration_months() == 24
        assert len(roadmap.phases) == 2

    def test_total_duration_months(self):
        roadmap = TransitionRoadmap(
            id="TR-002",
            name="Test",
            time_horizon_years=Decimal("1"),
            phases=[
                TransitionPhase(id="PH-01", name="P1", duration_months=3),
                TransitionPhase(id="PH-02", name="P2", duration_months=5),
                TransitionPhase(id="PH-03", name="P3", duration_months=2),
            ],
        )
        assert roadmap.total_duration_months() == 10

    def test_get_phase_at_month(self):
        roadmap = TransitionRoadmap(
            id="TR-002",
            name="Test",
            time_horizon_years=Decimal("1"),
            phases=[
                TransitionPhase(id="PH-01", name="P1", duration_months=3),
                TransitionPhase(id="PH-02", name="P2", duration_months=5),
                TransitionPhase(id="PH-03", name="P3", duration_months=2),
            ],
        )
        assert roadmap.get_phase_at_month(0).id == "PH-01"
        assert roadmap.get_phase_at_month(2).id == "PH-01"
        assert roadmap.get_phase_at_month(3).id == "PH-02"
        assert roadmap.get_phase_at_month(8).id == "PH-03"
        assert roadmap.get_phase_at_month(10) is None

    def test_empty_roadmap(self):
        roadmap = TransitionRoadmap(
            id="TR-003",
            name="Empty",
            time_horizon_years=Decimal("5"),
        )
        assert roadmap.total_duration_months() == 0
        assert roadmap.get_phase_at_month(0) is None
        assert roadmap.phases == []
