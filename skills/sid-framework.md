# SiD Framework — Systemic Design

## Overview

The **Symbiosis in Development (SiD)** framework, developed by Except Integrated Sustainability, is a systemic design methodology for tackling complex sustainability challenges. It integrates systems thinking, network theory, and design thinking to guide the transition from the current state to a desired regenerative state.

SiD operates through four sequential yet iterative phases: **Performative Goals**, **System Mapping**, **Network Parameters**, and **Transition Roadmaps**.

---

## 1. Performative Goals

### Concept
Performative Goals redefine traditional goal-setting. Instead of static, quantitative targets (e.g., "reduce CO2 by 20%"), performative goals describe **desired systemic behaviors and relationships** that the system should perform over time. They are:
- **Relational**: Define how system elements should interact.
- **Performance-oriented**: Describe ongoing behavior, not a one-time state.
- **Multi-scale**: Span environmental, social, economic, and cultural dimensions.
- **Adaptive**: Goals can evolve as the system learns.

### Structure
Each Performative Goal contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `name` | string | Short descriptive name |
| `dimension` | enum | `ECOLOGICAL`, `SOCIAL`, `ECONOMIC`, `CULTURAL`, `STRUCTURAL` |
| `description` | string | Long-form description of desired behavior |
| `stakeholders` | list[string] | Who is served by this goal |
| `key_performance_indicators` | list[KPI] | Measurable indicators tracking goal achievement |
| `time_horizon_years` | float | Planning horizon for this goal |
| `priority` | float (0–1) | Relative importance weight |
| `parent_goal_id` | string? | Link to parent goal in hierarchy |
| `conflicting_goals` | list[string] | Goals that may be in tension with this one |
| `synergistic_goals` | list[string] | Goals that reinforce this one |

### Example (for Syntropic Agroforestry)

```yaml
performative_goal:
  id: "PG-001"
  name: "Closed-loop biomass cycling"
  dimension: ECOLOGICAL
  description: >
    The agroforestry system maintains soil fertility entirely through
    internal biomass production, eliminating external fertilizer inputs.
    A-row prunings fully meet C-row nutrient demands on an ongoing basis.
  stakeholders: ["Farm operators", "Soil microbiome", "Downstream water users"]
  kpis:
    - name: "Biomass surplus ratio"
      unit: "ratio"
      target: "> 1.2"
    - name: "External fertilizer input"
      unit: "kg/ha/year"
      target: "= 0"
  time_horizon_years: 5
  priority: 1.0
  conflicting_goals: []
  synergistic_goals: ["PG-003", "PG-007"]
```

---

## 2. System Mapping

### Concept
System Mapping transforms the Performative Goals into a structured, quantifiable model of system elements and their interconnections. It creates a **network graph** of the system.

### Core Elements

#### Nodes (System Elements)
Every element in the system is a node with:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique node identifier |
| `name` | string | Descriptive name |
| `type` | enum | `STOCK`, `FLOW`, `ACTOR`, `CONSTRAINT`, `LEVERAGE_POINT`, `EXTERNALITY` |
| `dimension` | enum | Same as Performative Goal dimensions |
| `initial_value` | float? | Starting quantity (for stocks/flows) |
| `unit` | string | Unit of measurement |
| `boundary` | enum | `INTERNAL` (within system control) or `EXTERNAL` (outside) |
| `resilience` | float (0–1) | Capacity to absorb disturbance without regime shift |
| `description` | string | Narrative description |

#### Edges (Relationships)
Connections between nodes:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique edge identifier |
| `source_node_id` | string | Origin node |
| `target_node_id` | string | Destination node |
| `type` | enum | `CAUSAL_POSITIVE` (increase → increase), `CAUSAL_NEGATIVE` (increase → decrease), `MATERIAL_FLOW`, `INFORMATION_FLOW`, `ENERGY_FLOW`, `REGULATORY` |
| `strength` | float (-1 to 1) | Magnitude and direction of influence |
| `delay_months` | int | Time delay before effect manifests |
| `nonlinearity` | enum | `LINEAR`, `THRESHOLD`, `DIMINISHING_RETURNS`, `EXPONENTIAL` |
| `description` | string | Narrative of how source affects target |

### Causal Loop Diagrams (CLDs)
System maps support identification of:
- **Reinforcing Loops (R)**: Positive feedback that amplifies change (e.g., more biomass → more soil carbon → more growth → more biomass).
- **Balancing Loops (B)**: Negative feedback that stabilizes (e.g., more plants → more competition → slower growth → fewer plants).
- **Delays**: Time lags between action and effect (e.g., pruning today → nutrient availability after decomposition, ~45–90 days).

### Mapping Process
1. List all relevant system elements (brainstorming + stakeholder input).
2. Classify each element by type (stock, flow, actor, constraint, leverage point, externality).
3. Draw directed connections (edges) between elements.
4. Rate connection strength and identify delays.
5. Identify feedback loops and label them (R1, B1, etc.).
6. Validate with domain experts and refine.

---

## 3. Network Parameters

### Concept
Network Parameters are the quantitative metrics that describe the **state** of the system network at any point in time. They provide the "dashboard" for monitoring systemic health.

### Core Parameters

| Parameter | Unit | Description | Target Direction |
|-----------|------|-------------|-----------------|
| **Connectance** | ratio (0–1) | Proportion of possible connections that actually exist. `edges / (nodes * (nodes - 1))` | Moderate (0.1–0.3) — enough redundancy without chaos |
| **Modularity** | ratio (0–1) | Degree to which system can be decomposed into semi-independent sub-networks | High (0.3–0.7) — buffers against cascading failure |
| **Feedback Loops** | count | Number of reinforcing vs. balancing loops. Health requires balance (R ≈ B) | R/B ratio near 1.0 |
| **Resilience Index** | ratio (0–1) | Weighted average of node resilience scores | Maximize (> 0.6) |
| **Circularity** | ratio (0–1) | Proportion of material flows that are closed-loop within the system | Maximize (> 0.8) |
| **Diversity (Shannon Index)** | dimensionless | Species/element diversity: `-Σ(p_i * ln(p_i))` | Maximize |
| **Path Length (Average)** | count | Mean shortest path between any two nodes. Shorter = faster information/material transfer | Minimize (< 6) |
| **Centrality (Betweenness)** | ratio (0–1) | Identifies bottleneck nodes — nodes with highest betweenness are critical vulnerabilities | Monitor for single points of failure |
| **Synergy Density** | ratio | Proportion of synergistic relationships vs. total relationships | Maximize |
| **Leverage Potential** | ratio (0–1) | Weighted count of identified leverage points accessible to system actors | Maximize |

### For the Agroforestry Simulator
When combining with Syntropy:
- **Circularity** maps directly to the biomass surplus ratio.
- **Diversity** maps to strata occupation and species count per stratum.
- **Resilience** maps to successional redundancy (are there species ready to replace senescing ones?).
- **Path Length** maps to nutrient travel distance (A-row → decomposition → C-row uptake).

---

## 4. Transition Roadmaps

### Concept
A Transition Roadmap is a phased plan that moves the system from the **current state** (baseline) through intermediate states to the **desired state** defined by the Performative Goals. It is not a fixed blueprint but an **adaptive pathway** with decision points.

### Structure

```yaml
transition_roadmap:
  id: string
  name: string
  time_horizon_years: float
  phases:
    - id: string
      name: string              # e.g., "Phase 1: Placenta Establishment"
      duration_months: int
      baseline_state:
        node_values: map[string, float]    # Snapshot of key nodes at phase start
        network_parameters: map[string, float]  # Metrics snapshot
      target_state:
        node_values: map[string, float]
        network_parameters: map[string, float]
      interventions:
        - id: string
          name: string
          description: string
          affected_nodes: list[string]     # Nodes this intervention acts on
          affected_edges: list[string]     # Edges/relationships modified
          expected_impact: float (-1 to 1)  # Direction and magnitude of impact
          trigger_conditions: string        # When to execute (e.g., "month == 6 AND soil_cover < 0.8")
          cost: float                       # Resource cost
          duration_months: int              # How long intervention takes
          dependencies: list[string]        # Other interventions that must precede this
      decision_points:
        - id: string
          month: int
          condition: string     # e.g., "biomass_surplus_ratio > 1.2"
          if_true_proceed_to: string    # Phase ID if condition met
          if_false_proceed_to: string   # Phase ID if condition not met (adaptive branching)
      risks:
        - id: string
          description: string
          probability: float (0–1)
          impact: float (0–1)
          mitigation: string

```

### Phasing Principles
1. **No leapfrogging**: You can't skip from bare soil to Primary forest. Every stage builds on the previous.
2. **Minimum viable system first**: Phase 1 must establish the metabolic engine (A-rows producing > C-row demand) before any cash crop expansion.
3. **Trigger-based progression**: Phases don't advance by calendar alone — they advance when predefined **trigger conditions** are met.
4. **Adaptive branching**: If a phase fails to meet its targets, the roadmap offers an alternative path (adaptive management).
5. **Stakeholder feedback loops**: At each decision point, human stakeholders can override based on learning.

### Example Phase (for Syntropic Agroforestry)

```yaml
phase:
  id: "PH-01"
  name: "Soil Preparation & Placenta Establishment"
  duration_months: 6
  interventions:
    - id: "INT-001"
      name: "Plant pioneer A-rows"
      description: "Establish dense A-row planting with fast-growing N-fixing Placenta species at 0.5 m spacing."
      affected_nodes: ["soil_nitrogen", "soil_cover", "biomass_standing"]
      expected_impact: 0.7
      trigger_conditions: "month == 0"
      cost: 5000
      duration_months: 2
  decision_points:
    - id: "DP-001"
      month: 6
      condition: "soil_cover >= 0.8 AND soil_organic_carbon >= baseline_organic_carbon"
      if_true_proceed_to: "PH-02"
      if_false_proceed_to: "PH-01b"  # Remedial phase
```

---

## 5. Integration: SiD + Syntropy

When SiD is applied to Syntropic Agroforestry design:

| SiD Concept | Syntropy Mapping |
|-------------|-----------------|
| **Performative Goals** | System-wide objectives like "closed-loop biomass cycling", "complete strata occupation", "positive soil carbon trajectory" |
| **System Mapping** | Spatial graph of A-rows, C-rows, species as nodes; biomass flows, nutrient transfers, shading interactions as edges |
| **Network Parameters** | Biomass surplus ratio, strata diversity index, successional redundancy, circularity of nutrient flows |
| **Transition Roadmaps** | Phased planting plans: Placenta phase → Secondary I integration → Secondary II fruit production → Primary maturation. Each phase triggered by metabolic health checks. |

---

## References

- Except Integrated Sustainability. (2018). *SiD: Symbiosis in Development — Systemic Design Framework*. Amsterdam.
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green Publishing.
- Barabási, A.-L. (2016). *Network Science*. Cambridge University Press.
- Walker, B., & Salt, D. (2006). *Resilience Thinking*. Island Press.
