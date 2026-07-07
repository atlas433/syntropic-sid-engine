import pytest
from decimal import Decimal
from domain.entities.metabolic_loop import MetabolicFlow
from domain.value_objects.biomass import Biomass


class TestMetabolicFlow:
    def test_is_balanced_when_sufficient(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("100")),
            c_row_biomass_demand=Biomass(Decimal("80")),
            decomposition_rate=Decimal("0.85"),
        )
        assert flow.is_balanced

    def test_is_balanced_when_exact(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("100")),
            c_row_biomass_demand=Biomass(Decimal("85")),
            decomposition_rate=Decimal("0.85"),
        )
        assert flow.is_balanced

    def test_is_not_balanced_when_insufficient(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("50")),
            c_row_biomass_demand=Biomass(Decimal("80")),
            decomposition_rate=Decimal("0.85"),
        )
        assert not flow.is_balanced

    def test_is_not_balanced_with_low_decomposition(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("1000")),
            c_row_biomass_demand=Biomass(Decimal("200")),
            decomposition_rate=Decimal("0.05"),
        )
        assert not flow.is_balanced

    def test_bioavailable_biomass(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("100")),
            c_row_biomass_demand=Biomass(Decimal("80")),
            decomposition_rate=Decimal("0.85"),
        )
        assert flow.bioavailable_biomass == Biomass(Decimal("85"))

    def test_surplus(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("100")),
            c_row_biomass_demand=Biomass(Decimal("50")),
            decomposition_rate=Decimal("0.85"),
        )
        assert flow.surplus == Biomass(Decimal("35"))

    def test_no_surplus(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("50")),
            c_row_biomass_demand=Biomass(Decimal("80")),
            decomposition_rate=Decimal("0.85"),
        )
        assert flow.surplus == Biomass.ZERO

    def test_deficit(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("50")),
            c_row_biomass_demand=Biomass(Decimal("80")),
            decomposition_rate=Decimal("0.85"),
        )
        assert flow.deficit == Biomass(Decimal("37.5"))

    def test_no_deficit(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("200")),
            c_row_biomass_demand=Biomass(Decimal("80")),
            decomposition_rate=Decimal("0.85"),
        )
        assert flow.deficit == Biomass.ZERO

    def test_surplus_ratio(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("100")),
            c_row_biomass_demand=Biomass(Decimal("80")),
            decomposition_rate=Decimal("0.85"),
        )
        assert flow.surplus_ratio == Decimal("1.0625")

    def test_health_status_regenerative(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("200")),
            c_row_biomass_demand=Biomass(Decimal("80")),
            decomposition_rate=Decimal("0.85"),
        )
        assert flow.health_status == "REGENERATIVE"

    def test_health_status_sustainable(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("100")),
            c_row_biomass_demand=Biomass(Decimal("85")),
            decomposition_rate=Decimal("1.0"),
        )
        assert flow.health_status == "SUSTAINABLE"

    def test_health_status_strained(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("80")),
            c_row_biomass_demand=Biomass(Decimal("90")),
            decomposition_rate=Decimal("1.0"),
        )
        assert flow.health_status == "STRAINED"

    def test_health_status_mining(self):
        flow = MetabolicFlow(
            a_row_biomass_produced=Biomass(Decimal("30")),
            c_row_biomass_demand=Biomass(Decimal("100")),
            decomposition_rate=Decimal("1.0"),
        )
        assert flow.health_status == "MINING"
