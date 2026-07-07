import pytest
from decimal import Decimal
from domain.entities.roadmap import (
    TransitionPhase, TransitionRoadmap,
    Intervention, DecisionPoint, Risk,
    SolutionChannel, Governance,
)
from domain.entities.enums import ActionType, TransitionType


class TestIntervention:
    def test_create_intervention(self):
        iv = Intervention(
            id="INT-001",
            name="Plant pioneer A-rows",
            description="Establish dense A-row planting with fast-growing N-fixing species.",
            affected_nodes=["soil_nitrogen", "soil_cover", "biomass_standing"],
            affected_edges=["E-001"],
            action_type=ActionType.SYSTEMIC,
            expected_impact=Decimal("0.7"),
            trigger_conditions="month == 0",
            cost=Decimal("5000"),
            duration_months=2,
        )
        assert iv.name == "Plant pioneer A-rows"
        assert len(iv.affected_nodes) == 3
        assert iv.action_type == ActionType.SYSTEMIC
        assert iv.expected_impact == Decimal("0.7")

    def test_defaults(self):
        iv = Intervention(id="INT-002", name="Test", description="Test")
        assert iv.affected_nodes == []
        assert iv.affected_edges == []
        assert iv.action_type == ActionType.PULL
        assert iv.expected_impact == Decimal("0")
        assert iv.trigger_conditions == ""
        assert iv.cost == Decimal("0")
        assert iv.duration_months == 1
        assert iv.dependencies == []

    def test_action_types(self):
        iv_push = Intervention(id="I1", name="Push", description="",
                                action_type=ActionType.PUSH)
        iv_pull = Intervention(id="I2", name="Pull", description="",
                                action_type=ActionType.PULL)
        iv_lube = Intervention(id="I3", name="Lube", description="",
                                action_type=ActionType.LUBRICATE)
        iv_sys = Intervention(id="I4", name="Sys", description="",
                               action_type=ActionType.SYSTEMIC)
        assert iv_push.action_type == ActionType.PUSH
        assert iv_pull.action_type == ActionType.PULL
        assert iv_lube.action_type == ActionType.LUBRICATE
        assert iv_sys.action_type == ActionType.SYSTEMIC


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
            transition_type=TransitionType.START,
            interventions=[
                Intervention(id="INT-001", name="Plant pioneer A-rows",
                             description="Plant pioneer A-rows",
                             action_type=ActionType.SYSTEMIC,
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
        assert phase.transition_type == TransitionType.START

    def test_default_transition_type(self):
        phase = TransitionPhase(id="PH-02", name="Test", duration_months=3)
        assert phase.transition_type == TransitionType.CHANGE


class TestSolutionChannel:
    def test_create_channel(self):
        channel = SolutionChannel(
            id="SC-001",
            name="Biodiversity",
            phases=[
                TransitionPhase(id="PH-01", name="P1", duration_months=6),
            ],
        )
        assert channel.name == "Biodiversity"
        assert len(channel.phases) == 1

    def test_add_phase(self):
        channel = SolutionChannel(id="SC-002", name="Energy")
        phase = TransitionPhase(id="PH-01", name="Phase 1", duration_months=3)
        channel.add_phase(phase)
        assert len(channel.phases) == 1


class TestGovernance:
    def test_create_governance(self):
        gov = Governance(
            communication_plan="Monthly stakeholder newsletter",
            monitoring_frequency_months=3,
            stakeholder_updates=["Farm coop", "Local gov", "NGO partners"],
            budget_allocation=Decimal("50000"),
        )
        assert gov.monitoring_frequency_months == 3
        assert len(gov.stakeholder_updates) == 3
        assert gov.budget_allocation == Decimal("50000")

    def test_defaults(self):
        gov = Governance()
        assert gov.communication_plan == ""
        assert gov.monitoring_frequency_months == 3
        assert gov.stakeholder_updates == []
        assert gov.budget_allocation == Decimal("0")


class TestTransitionRoadmap:
    def test_create_roadmap(self):
        roadmap = TransitionRoadmap(
            id="TR-001",
            name="Full Syntropic Transition",
            time_horizon_years=Decimal("10"),
            solution_channels=[
                SolutionChannel(
                    id="SC-001",
                    name="Biodiversity",
                    phases=[
                        TransitionPhase(id="PH-01", name="Phase 1: Establishment", duration_months=6),
                        TransitionPhase(id="PH-02", name="Phase 2: Integration", duration_months=18),
                    ],
                ),
            ],
            governance=Governance(
                monitoring_frequency_months=6,
                budget_allocation=Decimal("100000"),
            ),
        )
        assert len(roadmap.solution_channels) == 1
        assert roadmap.total_duration_months() == 24
        phases = roadmap.get_all_phases()
        assert len(phases) == 2

    def test_total_duration_months(self):
        roadmap = TransitionRoadmap(
            id="TR-002",
            name="Test",
            time_horizon_years=Decimal("1"),
            solution_channels=[
                SolutionChannel(
                    id="SC-001",
                    name="A",
                    phases=[
                        TransitionPhase(id="PH-01", name="P1", duration_months=3),
                        TransitionPhase(id="PH-02", name="P2", duration_months=5),
                    ],
                ),
                SolutionChannel(
                    id="SC-002",
                    name="B",
                    phases=[
                        TransitionPhase(id="PH-03", name="P3", duration_months=2),
                    ],
                ),
            ],
        )
        assert roadmap.total_duration_months() == 10

    def test_get_phase_at_month(self):
        roadmap = TransitionRoadmap(
            id="TR-002",
            name="Test",
            time_horizon_years=Decimal("1"),
            solution_channels=[
                SolutionChannel(
                    id="SC-001",
                    name="A",
                    phases=[
                        TransitionPhase(id="PH-01", name="P1", duration_months=3),
                        TransitionPhase(id="PH-02", name="P2", duration_months=5),
                    ],
                ),
                SolutionChannel(
                    id="SC-002",
                    name="B",
                    phases=[
                        TransitionPhase(id="PH-03", name="P3", duration_months=2),
                    ],
                ),
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
        assert roadmap.solution_channels == []
        assert isinstance(roadmap.governance, Governance)
