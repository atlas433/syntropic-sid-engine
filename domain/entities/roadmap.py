from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Intervention:
    id: str
    name: str
    description: str
    affected_nodes: list[str] = field(default_factory=list)
    affected_edges: list[str] = field(default_factory=list)
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
    interventions: list[Intervention] = field(default_factory=list)
    decision_points: list[DecisionPoint] = field(default_factory=list)
    risks: list[Risk] = field(default_factory=list)
    baseline_node_values: dict[str, Decimal] = field(default_factory=dict)
    target_node_values: dict[str, Decimal] = field(default_factory=dict)
    baseline_network_params: dict[str, Decimal] = field(default_factory=dict)
    target_network_params: dict[str, Decimal] = field(default_factory=dict)


@dataclass
class TransitionRoadmap:
    id: str
    name: str
    time_horizon_years: Decimal
    phases: list[TransitionPhase] = field(default_factory=list)

    def total_duration_months(self) -> int:
        return sum(p.duration_months for p in self.phases)

    def get_phase_at_month(self, month: int) -> TransitionPhase | None:
        elapsed = 0
        for phase in self.phases:
            if elapsed <= month < elapsed + phase.duration_months:
                return phase
            elapsed += phase.duration_months
        return None
