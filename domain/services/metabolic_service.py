from dataclasses import dataclass, field
from decimal import Decimal
from typing import Protocol

from domain.entities.plant import Plant
from domain.entities.row import Row
from domain.entities.enums import RowType
from domain.entities.metabolic_loop import MetabolicFlow
from domain.value_objects.biomass import Biomass


class PlantRepository(Protocol):
    def find_by_row(self, row_id: str) -> list[Plant]: ...
    def save(self, plant: Plant) -> None: ...


class RowRepository(Protocol):
    def find_all(self) -> list[Row]: ...
    def find_by_type(self, row_type: RowType) -> list[Row]: ...
    def save(self, row: Row) -> None: ...


@dataclass
class MetabolicService:
    plant_repo: PlantRepository
    row_repo: RowRepository

    decomposition_rate: Decimal = field(default=Decimal("0.85"))
    default_c_row_demand_kg_per_m: Decimal = field(default=Decimal("8.0"))

    def simulate_month(self, month: int) -> MetabolicFlow:
        a_rows = self.row_repo.find_by_type(RowType.A)
        c_rows = self.row_repo.find_by_type(RowType.C)

        total_a_production = Biomass.ZERO
        total_c_demand = Biomass.ZERO

        for row in a_rows:
            for plant in row.plants:
                plant.grow()
                self.plant_repo.save(plant)
            biomass = row.get_total_biomass_production(month)
            total_a_production = total_a_production + Biomass(biomass)

        for row in c_rows:
            for plant in row.plants:
                plant.grow()
                self.plant_repo.save(plant)
            demand = row.total_biomass_demand
            total_c_demand = total_c_demand + Biomass(demand)

        total_a_production = total_a_production if total_a_production > Biomass.ZERO else Biomass(Decimal("0.001"))
        total_c_demand = total_c_demand if total_c_demand > Biomass.ZERO else Biomass(Decimal("0.001"))

        return MetabolicFlow(
            a_row_biomass_produced=total_a_production,
            c_row_biomass_demand=total_c_demand,
            decomposition_rate=self.decomposition_rate,
        )

    def evaluate_health(self, flow: MetabolicFlow) -> str:
        return flow.health_status
