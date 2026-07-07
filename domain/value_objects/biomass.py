from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class Biomass:
    """Weight of dry matter in kilograms. Immutable value object."""

    value_kg: Decimal

    ZERO: "Biomass" = None  # type: ignore

    def __post_init__(self):
        if self.value_kg < 0:
            raise ValueError(f"Biomass cannot be negative, got {self.value_kg}")

    def __add__(self, other: "Biomass") -> "Biomass":
        return Biomass(self.value_kg + other.value_kg)

    def __sub__(self, other: "Biomass") -> "Biomass":
        result = self.value_kg - other.value_kg
        return Biomass(max(Decimal("0"), result))

    def __mul__(self, factor: float) -> "Biomass":
        return Biomass(self.value_kg * Decimal(str(factor)))

    def __truediv__(self, other: "Biomass") -> Decimal:
        if other.value_kg == 0:
            return Decimal("Infinity")
        return self.value_kg / other.value_kg

    def ratio_to(self, other: "Biomass") -> Decimal:
        if other.value_kg == 0:
            return Decimal("0")
        return (self.value_kg / other.value_kg).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )

    def to_float(self) -> float:
        return float(self.value_kg)

    def __gt__(self, other: "Biomass") -> bool:
        return self.value_kg > other.value_kg

    def __ge__(self, other: "Biomass") -> bool:
        return self.value_kg >= other.value_kg

    def __lt__(self, other: "Biomass") -> bool:
        return self.value_kg < other.value_kg

    def __le__(self, other: "Biomass") -> bool:
        return self.value_kg <= other.value_kg

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Biomass):
            return NotImplemented
        return self.value_kg == other.value_kg


Biomass.ZERO = Biomass(Decimal("0"))


class BiomassPerLinearMeter:
    """Biomass per linear meter of row. Used for row-level metabolic calculations."""

    def __init__(self, kg_per_meter: Decimal):
        if kg_per_meter < 0:
            raise ValueError(
                f"Biomass per linear meter cannot be negative, got {kg_per_meter}"
            )
        self._kg_per_meter = kg_per_meter

    @property
    def kg_per_meter(self) -> Decimal:
        return self._kg_per_meter

    def for_row_length(self, length_m: Decimal) -> Biomass:
        return Biomass(self._kg_per_meter * length_m)

    def __add__(self, other: "BiomassPerLinearMeter") -> "BiomassPerLinearMeter":
        return BiomassPerLinearMeter(self._kg_per_meter + other._kg_per_meter)

    def __mul__(self, factor: float) -> "BiomassPerLinearMeter":
        return BiomassPerLinearMeter(self._kg_per_meter * Decimal(str(factor)))

    def __gt__(self, other: "BiomassPerLinearMeter") -> bool:
        return self._kg_per_meter > other._kg_per_meter

    def __ge__(self, other: "BiomassPerLinearMeter") -> bool:
        return self._kg_per_meter >= other._kg_per_meter

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BiomassPerLinearMeter):
            return NotImplemented
        return self._kg_per_meter == other._kg_per_meter
