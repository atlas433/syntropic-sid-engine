import pytest
from decimal import Decimal
from domain.entities.enums import (
    Stratum, SuccessionStage, LightRequirement, RowType,
    WaterRequirement, PruningRegime,
)
from domain.entities.species import SpeciesDefinition


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


class TestSpeciesDefinition:
    def test_species_creation(self, pioneer_species):
        assert pioneer_species.common_name == "Pigeon Pea"
        assert pioneer_species.stratum == Stratum.MEDIUM
        assert pioneer_species.nitrogen_fixation is True

    def test_biomass_per_meter(self, pioneer_species):
        bpm = pioneer_species.biomass_per_meter
        assert bpm.kg_per_meter == Decimal("4.5")

    def test_prune_biomass_aggressive(self, pioneer_species):
        result = pioneer_species.prune_biomass(pruning_intensity=0.6)
        assert result.kg_per_meter == Decimal("2.70")

    def test_prune_biomass_aggressive_capped(self, pioneer_species):
        result = pioneer_species.prune_biomass(pruning_intensity=1.0)
        assert result.kg_per_meter == Decimal("3.15")

    def test_prune_biomass_different_species(self, pioneer_species, fruit_tree_species, primary_tree_species):
        assert pioneer_species.prune_biomass(0.5).kg_per_meter == Decimal("2.25")
        assert fruit_tree_species.prune_biomass(0.5).kg_per_meter == Decimal("0.8")
        assert primary_tree_species.prune_biomass(0.5).kg_per_meter == Decimal("0")

    def test_prune_biomass_formative(self, fruit_tree_species):
        result = fruit_tree_species.prune_biomass()
        assert result.kg_per_meter == Decimal("0.8")

    def test_prune_biomass_none(self, primary_tree_species):
        result = primary_tree_species.prune_biomass()
        assert result.kg_per_meter == Decimal("0")
