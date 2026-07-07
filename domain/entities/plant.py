from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4

from domain.entities.species import SpeciesDefinition


@dataclass
class Plant:
    id: UUID
    species: SpeciesDefinition
    age_months: int = 0
    current_height_m: Decimal = Decimal("0.3")
    health_score: Decimal = Decimal("1.0")

    def grow(self, light_factor: Decimal = Decimal("1.0"),
             water_factor: Decimal = Decimal("1.0"),
             nutrient_factor: Decimal = Decimal("1.0")) -> None:
        growth = (
            self.species.growth_rate_cm_per_year
            / Decimal("12")
            * light_factor
            * water_factor
            * nutrient_factor
            * self.health_score
        )
        self.current_height_m += growth / Decimal("100")
        self.age_months += 1

    @property
    def is_mature(self) -> bool:
        return self.current_height_m >= self.species.mature_height_m * Decimal("0.9")

    @property
    def is_senescent(self) -> bool:
        return self.age_months >= int(self.species.lifecycle_years * 12)

    def should_prune(self, current_month: int) -> bool:
        regime = self.species.pruning_regime
        interval = self.species.pruning_interval_months
        from domain.entities.enums import PruningRegime
        if regime == PruningRegime.NONE:
            return False
        return current_month % interval == 0
