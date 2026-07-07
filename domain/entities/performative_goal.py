from dataclasses import dataclass, field
from decimal import Decimal

from domain.entities.enums import Dimension


@dataclass
class KPI:
    name: str
    unit: str
    target: str


@dataclass
class PerformativeGoal:
    id: str
    name: str
    dimension: Dimension
    description: str
    stakeholders: list[str] = field(default_factory=list)
    kpis: list[KPI] = field(default_factory=list)
    time_horizon_years: Decimal = Decimal("5")
    priority: Decimal = Decimal("1.0")
    parent_goal_id: str | None = None
    conflicting_goals: list[str] = field(default_factory=list)
    synergistic_goals: list[str] = field(default_factory=list)

    def is_high_priority(self) -> bool:
        return self.priority >= Decimal("0.8")

    def has_kpi(self, kpi_name: str) -> bool:
        return any(k.name == kpi_name for k in self.kpis)
