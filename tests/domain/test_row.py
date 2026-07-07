import pytest
from decimal import Decimal
from uuid import uuid4
from domain.entities.enums import (
    Stratum, SuccessionStage, LightRequirement, RowType,
    WaterRequirement, PruningRegime,
)
from domain.entities.species import SpeciesDefinition
from domain.entities.plant import Plant
from domain.entities.row import Row


@pytest.fixture
def pioneer_species():
    return SpeciesDefinition(
        id="SP-001",
        common_name="Pigeon Pea",
        scientific_name="Cajanus cajan",
        stratum=Stratum.MEDIUM,
        successional_stage=SuccessionStage.PLACENTA,
        lifecycle_years=Decimal("3"),
        growth_rate_cm_per_year=Decimal("200"),
        mature_height_m=Decimal("3"),
        canopy_diameter_m=Decimal("2"),
        biomass_production_kg_m_year=Decimal("4.5"),
        nitrogen_fixation=True,
        light_requirement=LightRequirement.HELIOPHILE,
        water_requirement=WaterRequirement.MEDIUM,
        mulch_quality_cn_ratio=Decimal("15"),
        harvestable_yield="pods, green manure",
        row_type=RowType.A,
        pruning_regime=PruningRegime.AGGRESSIVE,
        pruning_interval_months=3,
    )


@pytest.fixture
def fruit_tree_species():
    return SpeciesDefinition(
        id="SP-002",
        common_name="Avocado",
        scientific_name="Persea americana",
        stratum=Stratum.HIGH,
        successional_stage=SuccessionStage.SECONDARY_II,
        lifecycle_years=Decimal("40"),
        growth_rate_cm_per_year=Decimal("60"),
        mature_height_m=Decimal("10"),
        canopy_diameter_m=Decimal("8"),
        biomass_production_kg_m_year=Decimal("8.0"),
        nitrogen_fixation=False,
        light_requirement=LightRequirement.HELIOPHILE,
        water_requirement=WaterRequirement.HIGH,
        mulch_quality_cn_ratio=Decimal("40"),
        harvestable_yield="fruit",
        row_type=RowType.C,
        pruning_regime=PruningRegime.FORMATIVE,
        pruning_interval_months=12,
    )


@pytest.fixture
def primary_tree_species():
    return SpeciesDefinition(
        id="SP-003",
        common_name="Mahogany",
        scientific_name="Swietenia macrophylla",
        stratum=Stratum.EMERGENT,
        successional_stage=SuccessionStage.PRIMARY,
        lifecycle_years=Decimal("200"),
        growth_rate_cm_per_year=Decimal("40"),
        mature_height_m=Decimal("30"),
        canopy_diameter_m=Decimal("15"),
        biomass_production_kg_m_year=Decimal("20.0"),
        nitrogen_fixation=False,
        light_requirement=LightRequirement.HELIOPHILE,
        water_requirement=WaterRequirement.MEDIUM,
        mulch_quality_cn_ratio=Decimal("80"),
        harvestable_yield="timber",
        row_type=RowType.C,
        pruning_regime=PruningRegime.NONE,
        pruning_interval_months=0,
    )


class TestRow:
    def test_create_row(self):
        row = Row(id="R-001", row_type=RowType.A, length_m=Decimal("100"))
        assert row.row_type == RowType.A
        assert row.length_m == Decimal("100")
        assert row.plant_count == 0

    def test_add_plant(self, pioneer_species):
        row = Row(id="R-001", row_type=RowType.A, length_m=Decimal("100"))
        plant = Plant(id=uuid4(), species=pioneer_species)
        row.add_plant(plant)
        assert row.plant_count == 1

    def test_remove_plant(self, pioneer_species):
        row = Row(id="R-001", row_type=RowType.A, length_m=Decimal("100"))
        plant = Plant(id=uuid4(), species=pioneer_species)
        plant_id_str = str(plant.id)
        row.add_plant(plant)
        row.remove_plant(plant_id_str)
        assert row.plant_count == 0

    def test_total_biomass_production_no_plants(self):
        row = Row(id="R-001", row_type=RowType.A, length_m=Decimal("100"))
        assert row.get_total_biomass_production(month=0) == Decimal("0")

    def test_total_biomass_production_with_plants(self, pioneer_species):
        row = Row(id="R-001", row_type=RowType.A, length_m=Decimal("100"))
        for _ in range(5):
            row.add_plant(Plant(id=uuid4(), species=pioneer_species))
        total = row.get_total_biomass_production(month=0)
        assert total > Decimal("0")

    def test_total_biomass_demand(self):
        row = Row(id="R-002", row_type=RowType.C, length_m=Decimal("100"))
        assert row.total_biomass_demand == Decimal("800")

    def test_c_row_type(self):
        row = Row(id="R-002", row_type=RowType.C, length_m=Decimal("50"))
        assert row.row_type == RowType.C
        assert row.total_biomass_demand == Decimal("400")

    def test_initial_soil_organic_matter(self):
        row = Row(id="R-001", row_type=RowType.A, length_m=Decimal("100"))
        assert row.soil_organic_matter_kg_per_m == Decimal("5.0")
