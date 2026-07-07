from dataclasses import dataclass
from decimal import Decimal

from domain.value_objects.biomass import Biomass


@dataclass
class MetabolicFlow:
    a_row_biomass_produced: Biomass
    c_row_biomass_demand: Biomass
    decomposition_rate: Decimal

    @property
    def bioavailable_biomass(self) -> Biomass:
        """Biomass actually available to C-rows after decomposition."""
        return self.a_row_biomass_produced * float(self.decomposition_rate)

    @property
    def surplus(self) -> Biomass:
        available = self.bioavailable_biomass
        if available > self.c_row_biomass_demand:
            return available - self.c_row_biomass_demand
        return Biomass.ZERO

    @property
    def deficit(self) -> Biomass:
        available = self.bioavailable_biomass
        if available < self.c_row_biomass_demand:
            return self.c_row_biomass_demand - available
        return Biomass.ZERO

    @property
    def is_balanced(self) -> bool:
        """Core metabolic check: C-row biomass from A-rows >= C-row demand."""
        return self.bioavailable_biomass >= self.c_row_biomass_demand

    @property
    def surplus_ratio(self) -> Decimal:
        if self.c_row_biomass_demand == Biomass.ZERO:
            return Decimal("Infinity")
        return self.bioavailable_biomass.ratio_to(self.c_row_biomass_demand)

    @property
    def health_status(self) -> str:
        ratio = self.surplus_ratio
        if ratio >= Decimal("1.2"):
            return "REGENERATIVE"
        elif ratio >= Decimal("1.0"):
            return "SUSTAINABLE"
        elif ratio >= Decimal("0.8"):
            return "STRAINED"
        else:
            return "MINING"
