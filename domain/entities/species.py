from dataclasses import dataclass, field
from decimal import Decimal

from domain.entities.enums import (
    Stratum,
    SuccessionStage,
    LightRequirement,
    RowType,
    WaterRequirement,
    PruningRegime,
)
from domain.value_objects.biomass import BiomassPerLinearMeter


@dataclass
class SpeciesDefinition:
    id: str
    common_name: str
    scientific_name: str
    stratum: Stratum
    successional_stage: SuccessionStage
    lifecycle_years: Decimal
    growth_rate_cm_per_year: Decimal
    mature_height_m: Decimal
    canopy_diameter_m: Decimal
    biomass_production_kg_m_year: Decimal
    nitrogen_fixation: bool
    light_requirement: LightRequirement
    water_requirement: WaterRequirement
    mulch_quality_cn_ratio: Decimal
    harvestable_yield: str
    row_type: RowType
    pruning_regime: PruningRegime
    pruning_interval_months: int = 6

    @property
    def biomass_per_meter(self) -> BiomassPerLinearMeter:
        return BiomassPerLinearMeter(self.biomass_production_kg_m_year)

    def prune_biomass(self, pruning_intensity: float = 0.5) -> BiomassPerLinearMeter:
        """
        Calculate biomass yielded by pruning.
        pruning_intensity: fraction of above-ground biomass removed (0.0 to 1.0).
        """
        if self.pruning_regime == PruningRegime.NONE:
            return BiomassPerLinearMeter(Decimal("0"))
        if self.pruning_regime == PruningRegime.FORMATIVE:
            return self.biomass_per_meter * 0.1
        if self.pruning_regime == PruningRegime.SELECTIVE:
            return self.biomass_per_meter * min(pruning_intensity, 0.4)
        return self.biomass_per_meter * min(pruning_intensity, 0.7)
