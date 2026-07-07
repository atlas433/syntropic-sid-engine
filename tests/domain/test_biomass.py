import pytest
from decimal import Decimal
from domain.value_objects.biomass import Biomass


class TestBiomass:
    def test_create_valid(self):
        b = Biomass(Decimal("10.5"))
        assert b.value_kg == Decimal("10.5")

    def test_create_negative_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            Biomass(Decimal("-1"))

    def test_zero_is_zero(self):
        assert Biomass.ZERO.value_kg == Decimal("0")

    def test_addition(self):
        a = Biomass(Decimal("10"))
        b = Biomass(Decimal("15"))
        assert a + b == Biomass(Decimal("25"))

    def test_subtraction(self):
        a = Biomass(Decimal("20"))
        b = Biomass(Decimal("8"))
        assert a - b == Biomass(Decimal("12"))

    def test_subtraction_floor_at_zero(self):
        a = Biomass(Decimal("5"))
        b = Biomass(Decimal("10"))
        assert a - b == Biomass.ZERO

    def test_multiplication(self):
        a = Biomass(Decimal("10"))
        result = a * 0.5
        assert result == Biomass(Decimal("5"))

    def test_division(self):
        a = Biomass(Decimal("20"))
        b = Biomass(Decimal("5"))
        assert a / b == Decimal("4")

    def test_division_by_zero(self):
        a = Biomass(Decimal("10"))
        assert a / Biomass.ZERO == Decimal("Infinity")

    def test_ratio_to(self):
        produced = Biomass(Decimal("15"))
        demand = Biomass(Decimal("10"))
        assert produced.ratio_to(demand) == Decimal("1.5000")

    def test_gt_comparison(self):
        assert Biomass(Decimal("10")) > Biomass(Decimal("5"))
        assert not Biomass(Decimal("5")) > Biomass(Decimal("10"))

    def test_ge_comparison(self):
        assert Biomass(Decimal("10")) >= Biomass(Decimal("10"))
        assert Biomass(Decimal("10")) >= Biomass(Decimal("5"))

    def test_to_float(self):
        assert Biomass(Decimal("3.14")).to_float() == pytest.approx(3.14)

    def test_immutability(self):
        b = Biomass(Decimal("5"))
        with pytest.raises(AttributeError):
            b.value_kg = Decimal("10")
