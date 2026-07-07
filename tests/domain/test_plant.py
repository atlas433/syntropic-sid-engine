import pytest
from decimal import Decimal
from uuid import uuid4
from domain.entities.enums import (
    Stratum, SuccessionStage, LightRequirement, RowType,
    WaterRequirement, PruningRegime,
)
from domain.entities.species import SpeciesDefinition
from domain.entities.plant import Plant


@pytest.fixture
def pioneer_species():
    return SpeciesDefinition(
        id="SP-001",
        common_name="Pigeon Pea",
        scientific_name="Cajanus cajan",
        stratum=Stratum.MEDIUM,
        successional_stage=SuccessionStage.PLACENTA,
        lifecycle_years=Decimal("3"),
        growth_rate_cm_per_year=Decimal("240"),
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


class TestPlant:
    def test_create_plant(self, pioneer_species):
        plant = Plant(id=uuid4(), species=pioneer_species)
        assert plant.species.common_name == "Pigeon Pea"
        assert plant.age_months == 0
        assert plant.current_height_m == Decimal("0.3")
        assert plant.health_score == Decimal("1.0")

    def test_grow_full_conditions(self, pioneer_species):
        plant = Plant(id=uuid4(), species=pioneer_species)
        plant.grow()
        assert plant.age_months == 1
        assert plant.current_height_m > Decimal("0.3")

    def test_grow_specific_growth(self, pioneer_species):
        plant = Plant(id=uuid4(), species=pioneer_species)
        plant.grow(light_factor=Decimal("1.0"), water_factor=Decimal("1.0"), nutrient_factor=Decimal("1.0"))
        expected_growth_cm = Decimal("240") / Decimal("12")
        expected_height = (expected_growth_cm / Decimal("100")) + Decimal("0.3")
        assert plant.current_height_m == expected_height

    def test_grow_reduced_light(self, pioneer_species):
        plant = Plant(id=uuid4(), species=pioneer_species)
        plant.grow(light_factor=Decimal("0.5"))
        expected_growth_cm = (Decimal("240") / Decimal("12")) * Decimal("0.5")
        expected_height = (expected_growth_cm / Decimal("100")) + Decimal("0.3")
        assert plant.current_height_m == expected_height

    def test_grow_reduced_health(self, pioneer_species):
        plant = Plant(id=uuid4(), species=pioneer_species, health_score=Decimal("0.5"))
        plant.grow()
        expected_growth_cm = (Decimal("240") / Decimal("12")) * Decimal("0.5")
        expected_height = (expected_growth_cm / Decimal("100")) + Decimal("0.3")
        assert plant.current_height_m == expected_height

    def test_is_mature_false_initially(self, pioneer_species):
        plant = Plant(id=uuid4(), species=pioneer_species)
        assert not plant.is_mature

    def test_is_senescent_false_initially(self, pioneer_species):
        plant = Plant(id=uuid4(), species=pioneer_species)
        assert not plant.is_senescent

    def test_should_prune_aggressive_on_interval(self, pioneer_species):
        plant = Plant(id=uuid4(), species=pioneer_species)
        assert plant.should_prune(0)
        assert plant.should_prune(3)
        assert plant.should_prune(6)
        assert not plant.should_prune(1)
        assert not plant.should_prune(2)

    def test_should_prune_none_regime(self, primary_tree_species):
        plant = Plant(id=uuid4(), species=primary_tree_species)
        assert not plant.should_prune(0)
        assert not plant.should_prune(6)
