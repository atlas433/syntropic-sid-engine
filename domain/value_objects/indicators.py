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
class CraftdccvParameters:
    connectivity: Decimal
    redundancy: Decimal
    awareness: Decimal
    flexibility: Decimal
    transparency: Decimal
    diversity: Decimal
    complexity: Decimal
    centrality: Decimal
    variety: Decimal

    @property
    def resilience_score(self) -> Decimal:
        return (
            self.diversity * Decimal("0.25")
            + self.redundancy * Decimal("0.2")
            + self.flexibility * Decimal("0.2")
            + self.variety * Decimal("0.15")
            + (Decimal("1") - self.centrality) * Decimal("0.2")
        ).quantize(Decimal("0.001"))

    @property
    def is_healthy(self) -> bool:
        return self.resilience_score >= Decimal("0.6")


@dataclass(frozen=True)
class PeaieParameters:
    productivity: Decimal
    efficiency: Decimal
    autonomy: Decimal
    integrity: Decimal
    emergence: Decimal

    @property
    def performance_score(self) -> Decimal:
        return (
            self.productivity * Decimal("0.2")
            + self.efficiency * Decimal("0.25")
            + self.autonomy * Decimal("0.25")
            + self.integrity * Decimal("0.15")
            + self.emergence * Decimal("0.15")
        ).quantize(Decimal("0.001"))

    @property
    def is_healthy(self) -> bool:
        return self.performance_score >= Decimal("0.6")


@dataclass(frozen=True)
class SscneParameters:
    synergy: Decimal
    self_organization: Decimal
    synchronicity: Decimal
    nestedness: Decimal
    evolution: Decimal

    @property
    def dynamics_score(self) -> Decimal:
        return (
            self.synergy * Decimal("0.25")
            + self.self_organization * Decimal("0.25")
            + self.synchronicity * Decimal("0.15")
            + self.nestedness * Decimal("0.15")
            + self.evolution * Decimal("0.2")
        ).quantize(Decimal("0.001"))

    @property
    def is_healthy(self) -> bool:
        return self.dynamics_score >= Decimal("0.6")


@dataclass(frozen=True)
class NetworkParameters:
    craftdccv: CraftdccvParameters
    peaie: PeaieParameters
    sscne: SscneParameters
    reinforcing_loops: int = 0
    balancing_loops: int = 0

    @property
    def feedback_loop_ratio(self) -> Decimal:
        if self.balancing_loops == 0:
            return Decimal("Infinity")
        return (Decimal(str(self.reinforcing_loops)) / Decimal(str(self.balancing_loops))).quantize(Decimal("0.001"))

    @property
    def is_healthy(self) -> bool:
        return (
            self.craftdccv.is_healthy
            and self.peaie.is_healthy
            and self.sscne.is_healthy
        )

    @property
    def aggregate_score(self) -> Decimal:
        return (
            self.craftdccv.resilience_score * Decimal("0.4")
            + self.peaie.performance_score * Decimal("0.3")
            + self.sscne.dynamics_score * Decimal("0.3")
        ).quantize(Decimal("0.001"))
