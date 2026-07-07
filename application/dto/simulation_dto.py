from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SimulationStepDTO:
    month: int
    a_row_biomass_produced_kg: Decimal
    c_row_biomass_demand_kg: Decimal
    bioavailable_biomass_kg: Decimal
    surplus_kg: Decimal
    deficit_kg: Decimal
    surplus_ratio: Decimal
    health_status: str
    soil_organic_matter_kg_per_m: Decimal
    diversity_index: Decimal
