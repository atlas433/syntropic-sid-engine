from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class HealthIndicators:
    surplus_ratio: Decimal
    mulch_coverage_ratio: Decimal
    soil_carbon_trend: Decimal
    diversity_shannon_index: Decimal
    circularity: Decimal
    resilience_index: Decimal

    @property
    def is_metabolic_healthy(self) -> bool:
        return self.surplus_ratio >= Decimal("1.2") and self.mulch_coverage_ratio >= Decimal("1.0")

    @property
    def is_soil_healthy(self) -> bool:
        return self.soil_carbon_trend > 0

    @property
    def is_system_healthy(self) -> bool:
        return (
            self.is_metabolic_healthy
            and self.is_soil_healthy
            and self.resilience_index >= Decimal("0.6")
            and self.circularity >= Decimal("0.8")
        )


@dataclass(frozen=True)
class NetworkParameters:
    connectance: Decimal
    modularity: Decimal
    reinforcing_loops: int
    balancing_loops: int
    resilience_index: Decimal
    circularity: Decimal
    diversity_shannon_index: Decimal
    average_path_length: Decimal
    synergy_density: Decimal
    leverage_potential: Decimal

    @property
    def feedback_loop_ratio(self) -> Decimal:
        if self.balancing_loops == 0:
            return Decimal("Infinity")
        return (Decimal(str(self.reinforcing_loops)) / Decimal(str(self.balancing_loops))).quantize(Decimal("0.001"))

    @property
    def is_healthy(self) -> bool:
        return (
            Decimal("0.1") <= self.connectance <= Decimal("0.3")
            and Decimal("0.3") <= self.modularity <= Decimal("0.7")
            and self.resilience_index >= Decimal("0.6")
            and self.circularity >= Decimal("0.8")
            and self.average_path_length < Decimal("6")
        )
