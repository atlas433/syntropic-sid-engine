from dataclasses import dataclass, field
from decimal import Decimal

from domain.entities.performative_goal import PerformativeGoal
from domain.entities.system_map import SystemMap
from domain.entities.roadmap import Intervention


@dataclass(frozen=True)
class EvaluationResult:
    goals_achieved: bool
    unintended_consequences: list[str] = field(default_factory=list)
    needs_another_cycle: bool = True
    notes: str = ""


@dataclass
class SiDCycle:
    cycle_number: int
    days: int
    purpose: str = ""
    goals: list[PerformativeGoal] = field(default_factory=list)
    system_maps: list[SystemMap] = field(default_factory=list)
    understanding_notes: str = ""
    solutions: list[Intervention] = field(default_factory=list)
    evaluation: EvaluationResult | None = None

    @property
    def is_reconnaissance(self) -> bool:
        return self.cycle_number <= 2

    @property
    def is_deep_analysis(self) -> bool:
        return self.cycle_number >= 4

    def evaluate(self, goals_achieved: bool, notes: str = "",
                 unintended_consequences: list[str] = None,
                 needs_another_cycle: bool = True) -> None:
        self.evaluation = EvaluationResult(
            goals_achieved=goals_achieved,
            unintended_consequences=unintended_consequences or [],
            needs_another_cycle=needs_another_cycle,
            notes=notes,
        )


FIBONACCI_CYCLE_DURATIONS = {
    1: 1,
    2: 1,
    3: 2,
    4: 3,
    5: 5,
    6: 8,
    7: 13,
    8: 21,
}
