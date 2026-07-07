# Syntropic Agroforestry Rules

## Overview

Syntropic Agroforestry, developed by Ernst Götsch, is a form of regenerative agriculture that mimics natural forest succession to produce food while restoring ecosystems. It operates on four interdependent principles: **Strata** (spatial organization), **Succession** (temporal dynamics), **Patterns** (row configuration), and **Metabolism** (biomass cycling).

---

## 1. Strata — Vertical Layers

Every planting design must fill five vertical strata (layers), inspired by the structure of a mature forest. Each stratum occupies a distinct niche in the light profile.

| Stratum | Height Range | Role | Examples |
|---------|-------------|------|----------|
| **Emergent** | >8 m | Canopy dominants; long-cycle timber/fruit trees; provide structural frame | Eucalyptus, Mahogany, Jackfruit |
| **High** | 4–8 m | Secondary canopy; fruit/nut production; partial shade casters | Avocado, Citrus, Mango |
| **Medium** | 1.5–4 m | Sub-canopy shrubs; coffee, berries; nitrogen fixers | Coffee, Banana, Pigeon Pea |
| **Low** | 0.3–1.5 m | Herbaceous layer; vegetables, herbs, root crops | Cassava, Ginger, Pineapple |
| **Ground Cover** | <0.3 m | Soil protection; green manure; moisture retention | Sweet Potato, Arachis pintoi, Grasses |

### Rules
- Every planting row must eventually contain species from at least **four** of the five strata.
- Emergent species are planted at **wider spacing** (e.g., 8–10 m) to avoid overshading.
- Ground cover must be established within the **first 30 days** of planting to prevent soil exposure.
- Strata selection respects **light ecology**: heliophile (sun-loving) species go to emergent/high strata; sciophyte (shade-tolerant) species go to medium/low strata.

---

## 2. Succession — Temporal Stages

Succession describes the evolution of the system through time. Species are classified by their successional niche and lifecycle length.

### Stages

| Stage | Duration | Characteristics |
|-------|----------|-----------------|
| **Placenta (Pioneer)** | 0–2 years | Fast-growing colonizers; fix nitrogen aggressively; prepare soil; high biomass turnover; short lifespan (1–3 years) |
| **Secondary I** | 2–5 years | Early successional trees; medium growth rate; begin fruit production; lifespan 5–15 years |
| **Secondary II** | 5–15 years | Late successional trees; slower growth; long fruit-bearing period; lifespan 15–40 years |
| **Primary (Climax)** | 15–80+ years | Mature forest dominants; very slow initial growth; centuries-long lifespan; structural backbone |

### Rules
- **Placenta species** must be planted at **2–4x density** of other species to ensure rapid soil cover.
- When a plant completes its lifecycle (senescence), it is **pruned** (not removed), and its biomass becomes mulch on the C-row.
- **Staggered planting**: Secondary II and Primary species are planted simultaneously with Placenta — the Placenta provides shelter while slower species establish.
- Every species must be tagged with its stage: `PLACENTA`, `SECONDARY_I`, `SECONDARY_II`, or `PRIMARY`.
- Transitions: A species "graduates" to the next stage when:
  - Placenta → Secondary I: height exceeds 2 m
  - Secondary I → Secondary II: begins flowering/fruiting
  - Secondary II → Primary: reaches 60% of mature height

---

## 3. Patterns — A-Rows and C-Rows

The spatial layout follows alternating rows with distinct purposes.

### A-Row (Accumulation / Biomass Row)
- **Purpose**: Produce biomass for the entire system. These are the "engine" rows.
- **Composition**: Dominated by Placenta and fast-growing Secondary I species.
- **Function**: Dense planting of trees that are aggressively pruned to feed the C-rows.
- **Biomass output**: Measured in **kg of dry matter per linear meter per year**.
- **Pruning regime**: Every 3–6 months (Placenta), every 6–12 months (Secondary I).

### C-Row (Cash / Consumption Row)
- **Purpose**: Produce the marketable yield (fruit, timber, vegetables). These are the "solar panel" rows receiving the biomass.
- **Composition**: Secondary II and Primary species + Medium/Low strata crops.
- **Function**: Receives mulch from A-row prunings; higher light availability; produces food/cash crops.
- **Biomass demand**: Measured in **kg of dry matter per linear meter per year** needed to maintain fertility.

### Row Spacing Rules
- Standard spacing: **4 m between rows** (for tractor/management access).
- Pattern: A — C — A — C — A — C (alternating across the field).
- A-rows are narrower (dense planting within row) but same 4 m inter-row spacing.
- Within an A-row: spacing of 0.5–1 m between plants (dense for maximum biomass).
- Within a C-row: spacing depends on species mature size (e.g., fruit trees at 4–6 m, with understory crops between).

---

## 4. Metabolism — The Biomass/Mulching Loop

The metabolic loop is the core regenerative engine. It ensures that the system produces more fertility than it consumes.

### Core Equation

```
C_row_biomass_produced >= A_row_biomass_demand
```

For each time interval (monthly or quarterly), the system must check:

```
Σ (pruned_biomass * decomposition_rate) across all A-rows
    >=
Σ (crop_biomass_uptake + soil_organic_matter_loss) across all C-rows
```

### Key Parameters

| Parameter | Unit | Description |
|-----------|------|-------------|
| `pruned_biomass` | kg DM / linear meter | Dry matter produced by pruning a given species in a given time window |
| `decomposition_rate` | fraction (0–1) | Proportion of pruned biomass that mineralizes and becomes available to C-rows within the interval |
| `crop_biomass_uptake` | kg DM / linear meter | Biomass removed from C-row via harvest (exported from system) |
| `soil_organic_matter_loss` | kg DM / linear meter | Natural oxidation/decomposition loss of soil organic matter per interval |
| `biomass_surplus` | kg DM | Positive surplus enables system expansion; negative indicates fertility mining |

### Pruning Rules
- **Placenta pruning**: Cut at 50–70% of total above-ground biomass every 3–4 months. Material laid directly on the ground of the adjacent C-row.
- **Secondary I pruning**: Selectively thin 30–40% of branches every 6 months.
- **Secondary II**: Only formative pruning (shape maintenance), not for biomass.
- **Primary**: Never pruned for biomass. Only deadfall contributes.

### Metabolic Health Indicators
- **Surplus Ratio**: `biomass_surplus / C_row_demand`. Target > 0.2 (20% surplus).
- **Mulch Coverage**: `mulch_thickness_on_C_row / minimum_recommended_thickness`. Target > 1.0.
- **Soil Carbon Trend**: Year-over-year change in soil organic carbon. Must be positive.

---

## 5. Species Database Schema (Conceptual)

Each species in the system must have:

```yaml
species:
  id: string
  common_name: string
  scientific_name: string
  stratum: EMERGENT | HIGH | MEDIUM | LOW | GROUND_COVER
  successional_stage: PLACENTA | SECONDARY_I | SECONDARY_II | PRIMARY
  lifecycle_years: float          # Expected total lifespan
  growth_rate: float              # cm/year under optimal conditions
  mature_height_m: float          # Maximum mature height in meters
  canopy_diameter_m: float        # Mature canopy spread
  biomass_production_kg_m_year: float   # Dry matter produced per linear meter per year (when pruned)
  nitrogen_fixation: bool         # Is it a nitrogen fixer?
  light_requirement: HELIOPHILE | INTERMEDIATE | SCIOPHYTE
  water_requirement: HIGH | MEDIUM | LOW
  mulch_quality_cn_ratio: float   # C:N ratio of pruned material (lower = faster decomposition)
  harvestable_yield: string       # What is harvested (fruit, timber, leaf, root)
  row_type: A | C                 # Preferred row assignment

```

---

## 6. Simulation Time Steps

The simulator operates on a **monthly basis** as the base time step, with the following events per step:

1. **Growth Calculation**: Each plant grows according to its growth rate, moderated by light availability (neighboring strata), water stress, and nutrient availability.
2. **Pruning Event Check**: If month aligns with pruning schedule for a given species, trigger pruning.
3. **Biomass Transfer**: Pruned material from A-rows is distributed as mulch to adjacent C-rows.
4. **Metabolic Check**: Verify the core equation (`C_row_biomass_produced >= A_row_biomass_demand`).
5. **Succession Advancement**: Check if any plant meets criteria to advance to next successional stage.
6. **Yield Harvest**: If crops are at harvestable stage, record yield and update biomass export.
7. **Soil Update**: Update soil organic matter, moisture, and nutrient pools based on inputs and losses.

---

## References

- Götsch, E. (1995). *Breakthrough in Agriculture*. Fazenda Três Colinas.
- Andrade, D., Pasini, F., & Scarano, F. R. (2020). Syntropy and innovation in agriculture. *Current Opinion in Environmental Sustainability*, 45, 20-24.
- Miccolis, A. et al. (2016). *Agroforestry Systems for Ecological Restoration*. ICRAF.
