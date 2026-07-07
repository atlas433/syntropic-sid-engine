from dataclasses import dataclass, field
from decimal import Decimal
from math import log

from domain.entities.enums import RowType, Stratum, SuccessionStage
from domain.entities.row import Row
from domain.entities.species import SpeciesDefinition
from domain.services.metabolic_service import MetabolicService, RowRepository, PlantRepository
from domain.entities.metabolic_loop import MetabolicFlow
from domain.value_objects.indicators import NetworkParameters, HealthIndicators
from domain.entities.performative_goal import PerformativeGoal
from domain.entities.system_map import SystemMap
from domain.entities.roadmap import TransitionRoadmap
from domain.entities.cycle import SiDCycle
from application.dto.dashboard_dto import DashboardMetrics
from application.dto.row_dto import LayoutDTO, RowDTO, PlantDTO
from application.dto.simulation_dto import SimulationStepDTO


@dataclass
class DashboardUseCase:
    plant_repo: PlantRepository
    row_repo: RowRepository

    def build_metrics(
        self,
        current_month: int,
        species_catalog: list[SpeciesDefinition],
        goals: list[PerformativeGoal],
        system_map: SystemMap | None = None,
        roadmap: TransitionRoadmap | None = None,
        cycle: SiDCycle | None = None,
        network_params: NetworkParameters | None = None,
        health_indicators: HealthIndicators | None = None,
        monthly_history: list[MetabolicFlow] | None = None,
    ) -> DashboardMetrics:
        service = MetabolicService(
            plant_repo=self.plant_repo, row_repo=self.row_repo,
        )
        flow = service.simulate_month(current_month)

        rows = self.row_repo.find_all()
        a_rows = [r for r in rows if r.row_type == RowType.A]
        c_rows = [r for r in rows if r.row_type == RowType.C]
        all_plants = [p for r in rows for p in r.plants]
        species_ids = set(p.species.id for p in all_plants) if all_plants else set()

        strata_dist = {s.value: 0 for s in Stratum}
        succ_dist = {s.value: 0 for s in SuccessionStage}
        for p in all_plants:
            strata_dist[p.species.stratum.value] = strata_dist.get(p.species.stratum.value, 0) + 1
            succ_dist[p.species.successional_stage.value] = succ_dist.get(p.species.successional_stage.value, 0) + 1

        if monthly_history is None:
            monthly_history = []
        history_data = [
            {
                "month": i,
                "health": h.health_status if isinstance(h, MetabolicFlow) else "N/A",
                "surplus_ratio": float(h.surplus_ratio) if isinstance(h, MetabolicFlow) and not h.surplus_ratio.is_infinite() else 0.0,
            }
            for i, h in enumerate(monthly_history)
        ]

        species_data = [
            {"id": s.id, "name": s.common_name, "scientific": s.scientific_name,
             "stratum": s.stratum.value, "succession": s.successional_stage.value,
             "row_type": s.row_type.value, "n_fixer": s.nitrogen_fixation,
             "biomass_kg_m_year": float(s.biomass_production_kg_m_year)}
            for s in species_catalog
        ]

        goals_data = [
            {"id": g.id, "name": g.name, "level": g.level.value,
             "elsi": g.elsi_category.value, "description": g.description,
             "kpis": [{"name": k.name, "unit": k.unit, "target": k.target} for k in g.kpis],
             "priority": float(g.priority)}
            for g in goals
        ]

        params_craftdccv = {}
        params_peaie = {}
        params_sscne = {}
        if network_params:
            cp = network_params.craftdccv
            params_craftdccv = {
                "connectivity": float(cp.connectivity), "redundancy": float(cp.redundancy),
                "awareness": float(cp.awareness), "flexibility": float(cp.flexibility),
                "transparency": float(cp.transparency), "diversity": float(cp.diversity),
                "complexity": float(cp.complexity), "centrality": float(cp.centrality),
                "variety": float(cp.variety),
            }
            pp = network_params.peaie
            params_peaie = {
                "productivity": float(pp.productivity), "efficiency": float(pp.efficiency),
                "autonomy": float(pp.autonomy), "integrity": float(pp.integrity),
                "emergence": float(pp.emergence),
            }
            sp = network_params.sscne
            params_sscne = {
                "synergy": float(sp.synergy), "self_organization": float(sp.self_organization),
                "synchronicity": float(sp.synchronicity), "nestedness": float(sp.nestedness),
                "evolution": float(sp.evolution),
            }

        return DashboardMetrics(
            total_a_rows=len(a_rows),
            total_c_rows=len(c_rows),
            total_plants=len(all_plants),
            total_species=len(species_ids),
            a_row_biomass_produced_kg=flow.a_row_biomass_produced.value_kg,
            c_row_biomass_demand_kg=flow.c_row_biomass_demand.value_kg,
            surplus_ratio=flow.surplus_ratio if not flow.surplus_ratio.is_infinite() else Decimal("99"),
            health_status=flow.health_status,
            current_month=current_month,
            soil_organic_matter_kg_per_m=rows[0].soil_organic_matter_kg_per_m if rows else Decimal("5.0"),
            diversity_shannon_index=health_indicators.diversity_shannon_index if health_indicators else Decimal("0"),
            circularity=health_indicators.circularity if health_indicators else Decimal("0"),
            resilience_index=health_indicators.resilience_index if health_indicators else Decimal("0"),
            crafting_parameters=params_craftdccv,
            peaie_parameters=params_peaie,
            sscne_parameters=params_sscne,
            strata_distribution=strata_dist,
            succession_distribution=succ_dist,
            monthly_biomass_history=history_data,
            species_list=species_data,
            goals=goals_data,
            cycle_number=cycle.cycle_number if cycle else 1,
        )


@dataclass
class LayoutUseCase:
    row_repo: RowRepository

    def build_layout(self) -> LayoutDTO:
        rows = self.row_repo.find_all()
        row_dtos = []
        for row in rows:
            plant_dtos = [
                PlantDTO(
                    id=str(p.id), species_name=p.species.common_name,
                    stratum=p.species.stratum.value,
                    successional_stage=p.species.successional_stage.value,
                    age_months=p.age_months, current_height_m=p.current_height_m,
                    health_score=p.health_score, row_type=row.row_type.value,
                )
                for p in row.plants
            ]
            production = row.get_total_biomass_production(0) if row.row_type == RowType.A else Decimal("0")
            demand = row.total_biomass_demand if row.row_type == RowType.C else Decimal("0")
            row_dtos.append(RowDTO(
                id=row.id, row_type=row.row_type.value, length_m=row.length_m,
                plant_count=len(row.plants),
                soil_organic_matter_kg_per_m=row.soil_organic_matter_kg_per_m,
                plants=plant_dtos,
                biomass_production_kg_per_month=production,
                biomass_demand_kg_per_month=demand,
            ))

        max_length = max((r.length_m for r in rows), default=Decimal("100"))
        return LayoutDTO(
            rows=row_dtos, row_spacing_m=Decimal("4.0"),
            field_width_m=Decimal(len(rows)) * Decimal("4.0"),
            field_length_m=max_length,
        )


@dataclass
class SimulationUseCase:
    plant_repo: PlantRepository
    row_repo: RowRepository

    def simulate(self, months: int = 12) -> list[SimulationStepDTO]:
        service = MetabolicService(plant_repo=self.plant_repo, row_repo=self.row_repo)
        results: list[SimulationStepDTO] = []
        for month in range(months):
            flow = service.simulate_month(month)
            ratio = flow.surplus_ratio
            if ratio.is_infinite():
                ratio = Decimal("99")
            results.append(SimulationStepDTO(
                month=month,
                a_row_biomass_produced_kg=flow.a_row_biomass_produced.value_kg,
                c_row_biomass_demand_kg=flow.c_row_biomass_demand.value_kg,
                bioavailable_biomass_kg=flow.bioavailable_biomass.value_kg,
                surplus_kg=flow.surplus.value_kg,
                deficit_kg=flow.deficit.value_kg,
                surplus_ratio=ratio,
                health_status=flow.health_status,
                soil_organic_matter_kg_per_m=self._avg_som(),
                diversity_index=Decimal("2.45"),
            ))
        return results

    def _avg_som(self) -> Decimal:
        rows = self.row_repo.find_all()
        if not rows:
            return Decimal("5.0")
        total = sum((r.soil_organic_matter_kg_per_m for r in rows), Decimal("0"))
        return total / len(rows)
