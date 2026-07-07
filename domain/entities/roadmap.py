from dataclasses import dataclass, field
from decimal import Decimal

from domain.entities.enums import ActionType, TransitionType


@dataclass
class Intervention:
    id: str
    name: str
    description: str
    affected_nodes: list[str] = field(default_factory=list)
    affected_edges: list[str] = field(default_factory=list)
    action_type: ActionType = ActionType.PULL
    expected_impact: Decimal = Decimal("0")
    trigger_conditions: str = ""
    cost: Decimal = Decimal("0")
    duration_months: int = 1
    dependencies: list[str] = field(default_factory=list)


@dataclass
class DecisionPoint:
    id: str
    month: int
    condition: str
    if_true_proceed_to: str
    if_false_proceed_to: str


@dataclass
class Risk:
    id: str
    description: str
    probability: Decimal
    impact: Decimal
    mitigation: str

    @property
    def risk_score(self) -> Decimal:
        return (self.probability * self.impact).quantize(Decimal("0.001"))


@dataclass
class TransitionPhase:
    id: str
    name: str
    duration_months: int
    transition_type: TransitionType = TransitionType.CHANGE
    interventions: list[Intervention] = field(default_factory=list)
    decision_points: list[DecisionPoint] = field(default_factory=list)
    risks: list[Risk] = field(default_factory=list)
    baseline_node_values: dict[str, Decimal] = field(default_factory=dict)
    target_node_values: dict[str, Decimal] = field(default_factory=dict)
    baseline_network_params: dict[str, Decimal] = field(default_factory=dict)
    target_network_params: dict[str, Decimal] = field(default_factory=dict)


@dataclass
class SolutionChannel:
    id: str
    name: str
    phases: list[TransitionPhase] = field(default_factory=list)

    def add_phase(self, phase: TransitionPhase) -> None:
        self.phases.append(phase)


@dataclass
class Governance:
    communication_plan: str = ""
    monitoring_frequency_months: int = 3
    stakeholder_updates: list[str] = field(default_factory=list)
    budget_allocation: Decimal = Decimal("0")


@dataclass
class TransitionRoadmap:
    id: str
    name: str
    time_horizon_years: Decimal
    solution_channels: list[SolutionChannel] = field(default_factory=list)
    governance: Governance = field(default_factory=Governance)

    def total_duration_months(self) -> int:
        return sum(
            phase.duration_months
            for channel in self.solution_channels
            for phase in channel.phases
        )

    def get_all_phases(self) -> list[TransitionPhase]:
        return [
            phase
            for channel in self.solution_channels
            for phase in channel.phases
        ]

    def get_phase_at_month(self, month: int) -> TransitionPhase | None:
        elapsed = 0
        for channel in self.solution_channels:
            for phase in channel.phases:
                if elapsed <= month < elapsed + phase.duration_months:
                    return phase
                elapsed += phase.duration_months
        return None
