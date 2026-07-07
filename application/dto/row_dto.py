from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class PlantDTO:
    id: str
    species_name: str
    stratum: str
    successional_stage: str
    age_months: int
    current_height_m: Decimal
    health_score: Decimal
    row_type: str


@dataclass
class RowDTO:
    id: str
    row_type: str
    length_m: Decimal
    plant_count: int
    soil_organic_matter_kg_per_m: Decimal
    plants: list[PlantDTO] = field(default_factory=list)
    biomass_production_kg_per_month: Decimal = Decimal("0")
    biomass_demand_kg_per_month: Decimal = Decimal("0")


@dataclass
class LayoutDTO:
    rows: list[RowDTO] = field(default_factory=list)
    row_spacing_m: Decimal = Decimal("4.0")
    field_width_m: Decimal = Decimal("0")
    field_length_m: Decimal = Decimal("0")
