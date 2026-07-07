from dataclasses import dataclass, field
from decimal import Decimal

from domain.entities.enums import RowType
from domain.entities.plant import Plant


@dataclass
class Row:
    id: str
    row_type: RowType
    length_m: Decimal
    plants: list[Plant] = field(default_factory=list)
    soil_organic_matter_kg_per_m: Decimal = Decimal("5.0")

    @property
    def plant_count(self) -> int:
        return len(self.plants)

    def add_plant(self, plant: Plant) -> None:
        self.plants.append(plant)

    def remove_plant(self, plant_id: str) -> None:
        self.plants = [p for p in self.plants if str(p.id) != plant_id]

    def get_total_biomass_production(self, month: int) -> Decimal:
        total = Decimal("0")
        for plant in self.plants:
            if plant.should_prune(month):
                species_def = plant.species
                regime = species_def.pruning_regime
                from domain.entities.enums import PruningRegime
                if regime == PruningRegime.AGGRESSIVE:
                    intensity = 0.6
                elif regime == PruningRegime.SELECTIVE:
                    intensity = 0.35
                elif regime == PruningRegime.FORMATIVE:
                    intensity = 0.1
                else:
                    intensity = 0.0
                total += species_def.prune_biomass(intensity).kg_per_meter
        return total * self.length_m

    @property
    def total_biomass_demand(self) -> Decimal:
        return self.length_m * Decimal("8.0")
