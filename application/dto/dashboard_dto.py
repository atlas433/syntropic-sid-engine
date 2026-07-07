from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class DashboardMetrics:
    total_a_rows: int = 0
    total_c_rows: int = 0
    total_plants: int = 0
    total_species: int = 0
    a_row_biomass_produced_kg: Decimal = Decimal("0")
    c_row_biomass_demand_kg: Decimal = Decimal("0")
    surplus_ratio: Decimal = Decimal("0")
    health_status: str = "UNKNOWN"
    current_month: int = 0
    soil_organic_matter_kg_per_m: Decimal = Decimal("5.0")
    diversity_shannon_index: Decimal = Decimal("0")
    circularity: Decimal = Decimal("0")
    resilience_index: Decimal = Decimal("0")
    crafting_parameters: dict[str, Decimal] = field(default_factory=dict)
    peaie_parameters: dict[str, Decimal] = field(default_factory=dict)
    sscne_parameters: dict[str, Decimal] = field(default_factory=dict)
    strata_distribution: dict[str, int] = field(default_factory=dict)
    succession_distribution: dict[str, int] = field(default_factory=dict)
    monthly_biomass_history: list[dict] = field(default_factory=list)
    species_list: list[dict] = field(default_factory=list)
    goals: list[dict] = field(default_factory=list)
    cycle_number: int = 1
