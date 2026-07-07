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
from domain.services.metabolic_service import MetabolicService
from infrastructure.repositories.in_memory import (
    InMemoryPlantRepository,
    InMemoryRowRepository,
)


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
def setup_system(pioneer_species, fruit_tree_species):
    plant_repo = InMemoryPlantRepository()
    row_repo = InMemoryRowRepository()

    a_row = Row(id="A-1", row_type=RowType.A, length_m=Decimal("100"))
    c_row = Row(id="C-1", row_type=RowType.C, length_m=Decimal("100"))

    for i in range(50):
        plant = Plant(id=uuid4(), species=pioneer_species)
        a_row.add_plant(plant)
        plant_repo.save(plant)

    for i in range(10):
        plant = Plant(id=uuid4(), species=fruit_tree_species)
        c_row.add_plant(plant)
        plant_repo.save(plant)

    row_repo.save(a_row)
    row_repo.save(c_row)

    return plant_repo, row_repo


class TestMetabolicService:
    def test_simulate_month_returns_flow(self, setup_system):
        plant_repo, row_repo = setup_system
        service = MetabolicService(plant_repo=plant_repo, row_repo=row_repo)
        flow = service.simulate_month(month=0)
        assert flow is not None
        assert flow.a_row_biomass_produced > flow.c_row_biomass_demand

    def test_health_status_is_regenerative_with_enough_a_rows(self, setup_system):
        plant_repo, row_repo = setup_system
        service = MetabolicService(plant_repo=plant_repo, row_repo=row_repo)
        flow = service.simulate_month(month=0)
        assert flow.health_status == "REGENERATIVE"

    def test_pruning_months_are_regenerative(self, setup_system):
        plant_repo, row_repo = setup_system
        service = MetabolicService(plant_repo=plant_repo, row_repo=row_repo)
        for month in (0, 3, 6, 9):
            flow = service.simulate_month(month=month)
            assert flow.health_status in ("REGENERATIVE", "SUSTAINABLE")

    def test_insufficient_a_rows_causes_mining(self, pioneer_species, fruit_tree_species):
        plant_repo = InMemoryPlantRepository()
        row_repo = InMemoryRowRepository()

        a_row = Row(id="A-1", row_type=RowType.A, length_m=Decimal("10"))
        c_row = Row(id="C-1", row_type=RowType.C, length_m=Decimal("100"))

        plant = Plant(id=uuid4(), species=pioneer_species)
        a_row.add_plant(plant)
        plant_repo.save(plant)

        for _ in range(20):
            plant = Plant(id=uuid4(), species=fruit_tree_species)
            c_row.add_plant(plant)
            plant_repo.save(plant)

        row_repo.save(a_row)
        row_repo.save(c_row)

        service = MetabolicService(plant_repo=plant_repo, row_repo=row_repo)
        flow = service.simulate_month(month=0)
        assert flow.health_status == "MINING"
