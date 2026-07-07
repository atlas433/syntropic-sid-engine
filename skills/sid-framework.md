# SiD Framework — Symbiosis in Development

## Overview

The **Symbiosis in Development (SiD)** framework, developed by Except Integrated Sustainability, is a systemic design methodology for tackling complex sustainability challenges. It integrates systems thinking, network theory, and design thinking to guide the transition from the current state to a desired regenerative state.

SiD operates through **five sequential yet iterative steps**:

1. **Goals, Vision & Indicators** — Where do we want to go?
2. **System Mapping** — Where are we now?
3. **System Understanding** — What does it all mean?
4. **Solutioning & Roadmapping** — How do we get there?
5. **Evaluate & Iterate** — Are we going the right way?

The method is inherently **cyclical**: each cycle deepens understanding. A minimum of 3 cycles is recommended; larger projects may run 8+. Cycle lengths can be planned using the **Fibonacci sequence** (1, 1, 2, 3, 5, 8, 13, 21 days). The first cycle is a "reconnaissance" — done quickly with the full team to survey the challenge.

---

## Scoping: The SiD Hierarchy

Before detailed work begins, scope is set across two axes:

### Vertical Scope (SNO Levels)
| Level | Focus | Example |
|-------|-------|---------|
| **System** | Holistic behavior, emergence, overall performance | "The neighborhood as a living system" |
| **Network** | Relationships, flows, structure | "Energy and material flows between buildings" |
| **Object** | Individual elements, components | "A specific building's solar array" |

Goals must be set at **System level** (performative, not prescriptive). Sub-goals are set at Network and Object levels.

### Horizontal Scope (ELSI Categories)
ELSI indexes system analysis across **8 categories** in 4 pairs:

| Pair | Category | Category | Domain |
|------|----------|----------|--------|
| **Energy & Materials** | Energy | Materials | Physical resources, flows, infrastructure |
| **Ecosystems & Species** | Ecosystems | Species | Biodiversity, ecology, natural systems |
| **Culture & Economy** | Culture | Economy | Social fabric, economic activity, values |
| **Health & Happiness** | Health | Happiness | Wellbeing, fulfillment, quality of life |

ELSI ensures all dimensions of sustainability are covered and prevents externalizing problems by omitting categories.

---

## 1. Step 1: Goals, Vision & Indicators

### Concept
Performative Goals describe **desired systemic behaviors** — not static targets. They answer "Where do we really want to go?" Goals should be:
- **System-level**: Reflect the system's purpose, not a specific solution
- **Performative**: Describe ongoing behavior, not a one-time state or prescriptive solution
- **Multi-scale**: Span environmental, social, economic, and cultural dimensions
- **Adaptive**: Can evolve as understanding deepens

### Key Principles
- **Never prescribe the solution in the goal formulation** — this reduces solution space. Bad: "All buildings should use solar panels." Good: "The neighborhood provides its own renewable energy." Better (system level): "The neighborhood is energy-autonomous and resilient."
- **"Flip" the goal when needed**: If a goal focuses on an object (e.g., "Make the transport system sustainable"), reframe it to system level ("Increase city sustainability by means of the transport system").
- **Use ELSI + Network Parameters** to formulate sub-goals and ensure completeness.

### Components
| Component | Description |
|-----------|-------------|
| **System-level goal** | The overarching destination — broad and ambitious |
| **Network-level sub-goals** | Relationship-focused (e.g., "Close all material cycles") |
| **Object-level sub-goals** | Element-focused, structured by ELSI |
| **Vision** (optional) | Qualitative horizon point — can be movies, stories, drawings |
| **Project boundaries** | Time, budget, team, resources (edge conditions) |
| **System boundary** | What's inside vs. outside the system under investigation |
| **KPIs** | Developed in later cycles to measure goal achievement |

### Setting System Boundaries
- Boundaries are not singular — set them in time, space, and per sub-goal
- They should be **as large as necessary for adequate solutions, small enough to be manageable**
- Boundaries are adjusted iteratively as understanding grows
- The bigger the boundary, the larger the solution space but also the effort required

### Structure
Each Performative Goal contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `name` | string | Short descriptive name |
| `level` | enum | `SYSTEM`, `NETWORK`, `OBJECT` |
| `elsi_category` | enum | `ENERGY`, `MATERIALS`, `ECOSYSTEMS`, `SPECIES`, `CULTURE`, `ECONOMY`, `HEALTH`, `HAPPINESS` |
| `description` | string | Long-form performative description |
| `stakeholders` | list[string] | Who is served by this goal |
| `key_performance_indicators` | list[KPI] | Measurable indicators |
| `time_horizon_years` | float | Planning horizon |
| `priority` | float (0–1) | Relative importance weight |
| `parent_goal_id` | string? | Link to parent goal in hierarchy |
| `conflicting_goals` | list[string] | Goals that may be in tension |
| `synergistic_goals` | list[string] | Goals that reinforce this one |

### Example (for Syntropic Agroforestry)

```yaml
performative_goal:
  id: "PG-001"
  name: "Closed-loop biomass cycling"
  level: SYSTEM
  elsi_category: ECOSYSTEMS
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

## 2. Step 2: System Mapping

### Concept
System Mapping transforms goals into a structured, visual model of system elements and their interconnections. It creates a **network graph** of the system across three dimensions.

### Three Mapping Dimensions
| Dimension | Description | Examples |
|-----------|-------------|----------|
| **Time** | Temporal relationships, trends, evolution | Timelines, trend graphs, project phasing |
| **Space** | Geographical, spatial relationships | Land-use maps, floorplans, regional maps |
| **Context** | Causal, relational, conceptual relationships | Causal loop diagrams, flow maps, stakeholder maps |

Each dimension is mapped at **three scales** (small, medium, large), yielding a 3x3 "Map of Maps" grid with 9 mapping areas. This ensures multi-scale coverage.

### Mapping Process
1. **Determine subject and goal** — What are we mapping and why?
2. **Create a Map of Maps** — Decide what maps to make across the 3x3 grid
3. **Sketch all maps roughly** — Quick, low-detail passes across all 9 areas; use ELSI8 to ensure full coverage
4. **Select and refine** — Keep promising maps, merge overlapping ones, research missing data
5. **Finalize** — Polish representation, involve stakeholders for validation

### Standard Map Types
| Map Type | Dimension | Description |
|----------|-----------|-------------|
| Material & Energy Flow Map | Context | Sankey diagrams of resource flows |
| Causal Loop Diagram | Context | Nodes and directed edges showing feedback |
| Stakeholder Map | Context | Actors and their relationships to the challenge |
| Organizational Hierarchy | Context | Control and reporting structures |
| Trend Map | Time | Historical graph of critical parameters |
| Project Timeline / Routemap | Time | Intended actions toward the goal |
| Programmatic Plan Map | Space | Spatial distribution of program elements |

### Core Elements

#### Nodes (System Elements)
Every element in the system is a node:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique node identifier |
| `name` | string | Descriptive name |
| `type` | enum | `STOCK`, `FLOW`, `ACTOR`, `CONSTRAINT`, `LEVERAGE_POINT`, `EXTERNALITY` |
| `elsi_category` | enum | ELSI8 category |
| `scope` | enum | `OBJECT`, `NETWORK`, `SYSTEM` |
| `boundary` | enum | `INTERNAL` (within system boundary) or `EXTERNAL` (outside) |
| `initial_value` | float? | Starting quantity (for stocks/flows) |
| `unit` | string | Unit of measurement |
| `resilience` | float (0–1) | Capacity to absorb disturbance |
| `description` | string | Narrative description |

#### Edges (Relationships)
Connections between nodes:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique edge identifier |
| `source_node_id` | string | Origin node |
| `target_node_id` | string | Destination node |
| `type` | enum | `CAUSAL_POSITIVE`, `CAUSAL_NEGATIVE`, `MATERIAL_FLOW`, `INFORMATION_FLOW`, `ENERGY_FLOW`, `REGULATORY` |
| `strength` | float (-1 to 1) | Magnitude and direction of influence |
| `delay_months` | int | Time delay before effect manifests |
| `nonlinearity` | enum | `LINEAR`, `THRESHOLD`, `DIMINISHING_RETURNS`, `EXPONENTIAL` |
| `description` | string | Narrative of how source affects target |

### Causal Loop Diagrams (CLDs)
System maps support identification of:
- **Reinforcing Loops (R)**: Positive feedback amplifying change
- **Balancing Loops (B)**: Negative feedback stabilizing the system
- **Delays**: Time lags between action and effect

### Account for Externalities
Always mark elements outside the system boundary that influence the system. They cannot be quantified precisely but must be acknowledged to inform thinking.

---

## 3. Step 3: System Understanding

### Concept
After mapping, take a step back to **develop intuitive understanding** through immersion. The goal is to let the system "come alive" mentally — bottom-up maps meet top-down understanding to generate deeper insight. Solutions often emerge naturally from this phase.

### Methods
| Method | Description |
|--------|-------------|
| **Relax & Reflect** | Take downtime — walk in nature, let the subconscious process. Archimedes' "Eureka" moment. |
| **Play & Learn** | Experiment with the system through games, creative exercises |
| **Talk & Reconsider** | Discuss with others; explain the system to outsiders; involve external experts |
| **Serious Gaming** | Structured simulations of complex social/policy/economic dynamics |
| **Role Reversal** | Adopt stakeholder positions and maximize their interests in interaction |
| **Simulation** | Computer models (thermal analysis, agent-based modeling) to explore behavior |

### Structured Exercises

#### Climbing the Mountain of Understanding
Walk mentally from object level → network level → system level (holistic overview), then back down to object level with new insights. This develops the ability to see how high-level patterns manifest in material reality.

#### Walking Down SiD Road
Probe the system by asking "what if" questions against each network parameter:
- What if we increase **transparency**? What happens?
- What drives **resilience** in this system?
- How do **ecosystems** influence network **diversity**?
- Where are **bottlenecks** (centrality)? What if they're removed?

#### VSM (Viable Systems Model)
For organizational/logistical systems, use Stafford Beer's VSM (1972) for bottom-up network analysis. Combines well with SiD's qualitative approaches.

### Key Insight
This phase requires **mental rest** — it is not optional. Insight comes when the brain has time to synthesize mapped complexity into intuitive understanding. Group exercises + solitary reflection are both needed.

---

## 4. Step 4: Solutioning & Roadmapping

### Concept
Find actions to move the system from its current state to the desired state defined by goals. Solutions are **ingredients**; the roadmap is the **recipe** that combines them in time.

### 4.1 System-Level Solutioning Approaches

#### Block Transition Strategy
Treat system agents as blocks on a table connected by rubber bands:
1. **Determine the agents** — Map stakeholders and their relationships
2. **Create awareness** — Give key actors "change energy" and desire to move
3. **Align goals** — Ensure agents pull in the same direction
4. **Enabling actions** — Move the system with four action types:
   - **Pull**: Incentives, carrots, attractive benefits
   - **Push**: Regulation, fines, confrontation
   - **Lubricate**: Reduce friction — best practices, tools, guidelines
   - **Tilt the table (Systemic action)**: Change the whole playing field — laws, breakthrough innovation

#### Before/After Solution Maps
Create system maps of the desired state and compare with current state maps. Identify what must change and which levers can shift the system.

#### Largest Factor Approach
Identify the biggest drivers or barriers in the system and focus effort there. Look for threshold effects where small changes yield large results.

#### Internalizing External Resources
Find resources currently outside the system boundary (waste streams, underused assets) and bring them in. Cross-breed every asset with every other to find novel syntheses.

#### Re-visioning
Examine whether the system's fundamental purpose should change — not improving the existing system but transitioning to a different one.

#### Training the System
For advanced practitioners: identify system behaviors that can be "boosted" toward the goal via network parameter optimization.

### 4.2 Network-Level Solutioning (Parameter Optimization)

Optimize network parameters systematically by asking targeted questions:
- **CRAFTDCCV set** (Connectivity, Redundancy, Awareness, Flexibility, Transparency, Diversity, Complexity, Centrality, Variety)
- **PEAIE set** (Productivity, Efficiency, Autonomy, Integrity, Emergence)
- **SSCNE set** (Synergy, Self-organization, Synchronicity, Nestedness, Evolution)

For each parameter, ask: "What is its current state? What is the ideal state? What actions can improve it?"

### 4.3 Object-Level Solutioning (Gap Finding)

#### Gap Finding & Closing Loops
Look for missing connections and open resource loops. Where do flows "escape" the system? Where are connections that should exist but don't?

### 4.4 Roadmapping

Once solutions are identified, sequence them into a roadmap.

#### Ten Steps to a Roadmap
1. **List all actions and solutions** — On post-its, everything from object fixes to systemic interventions
2. **Cluster actions** — Group related actions thematically
3. **Identify major solution channels** — High-level streams of work (e.g., Energy, Water, Governance, Education)
4. **Place actions on timeline** — Near-term (firm), medium-term, long-term (flexible)
5. **Cluster within channels** — Organize each channel's items in sequence
6. **Adjust, identify and solve missing steps** — Fill gaps; add governance and management actions
7. **Identify transition phase** — Label each action by transition type (stop, start, change, etc.)
8. **Add governance channels** — Communication, monitoring, stakeholder management, finance
9. **Set responsibilities and governance** — Who owns what, approval gates, review cycles
10. **Formalize, document, and get approval** — Finalize for communication and execution

#### Roadmap Principles
- **Near-term actions are firm**; further in the future, plans become flexible
- **Trigger-based progression**: don't advance by calendar alone — advance when predefined conditions are met
- **Adaptive**: review and update cycles are built in
- The roadmap is also a **stakeholder communication tool**

### Structure

```yaml
transition_roadmap:
  id: string
  name: string
  time_horizon_years: float
  solution_channels:
    - id: string
      name: string                      # e.g., "Energy", "Biodiversity", "Governance"
      phases:
        - id: string
          name: string                  # e.g., "Phase 1: Placenta Establishment"
          duration_months: int
          transition_type: enum         # START, STOP, CHANGE, ENABLE, GOVERN
          baseline_state:
            node_values: map[string, float]
            network_parameters: map[string, float]
          target_state:
            node_values: map[string, float]
            network_parameters: map[string, float]
          interventions:
            - id: string
              name: string
              description: string
              affected_nodes: list[string]
              affected_edges: list[string]
              action_type: enum         # PUSH, PULL, LUBRICATE, SYSTEMIC
              expected_impact: float (-1 to 1)
              trigger_conditions: string
              cost: float
              duration_months: int
              dependencies: list[string]
          decision_points:
            - id: string
              month: int
              condition: string
              if_true_proceed_to: string
              if_false_proceed_to: string
          risks:
            - id: string
              description: string
              probability: float (0–1)
              impact: float (0–1)
              mitigation: string
      governance:
        communication_plan: string
        monitoring_frequency_months: int
        stakeholder_updates: list[string]
        budget_allocation: float
```

### Example Phase (for Syntropic Agroforestry)

```yaml
phase:
  id: "PH-01"
  name: "Soil Preparation & Placenta Establishment"
  duration_months: 6
  transition_type: START
  interventions:
    - id: "INT-001"
      name: "Plant pioneer A-rows"
      description: "Establish dense A-row planting with fast-growing N-fixing Placenta species at 0.5 m spacing."
      affected_nodes: ["soil_nitrogen", "soil_cover", "biomass_standing"]
      action_type: SYSTEMIC
      expected_impact: 0.7
      trigger_conditions: "month == 0"
      cost: 5000
      duration_months: 2
  decision_points:
    - id: "DP-001"
      month: 6
      condition: "soil_cover >= 0.8 AND soil_organic_carbon >= baseline_organic_carbon"
      if_true_proceed_to: "PH-02"
      if_false_proceed_to: "PH-01b"
```

---

## 5. Step 5: Evaluate & Iterate

### Concept
Reflect on the cycle's outputs, compare solutions to goals, and determine if another cycle is needed. Evaluation differs by stage: early cycles need only direction-checking; later cycles require rigorous KPI verification.

### Core Questions
1. **"Did we achieve our goals with the chosen solutions, within the chosen boundaries?"**
2. **"What are potential unintended consequences of the solutions on the system and all stakeholders?"**

### Evaluation Methods

| Method | Description |
|--------|-------------|
| **Evaluation Matrix** | Score each solution against all goals and edge conditions. Compare competing solutions. |
| **System Impact Check** | Map the ripple effects of solutions through the system — what unintended dynamics might emerge? |
| **External Evaluation** | Bring in a panel of outside experts for fresh eyes |
| **Mid-Session Harvests** | Every half-day, recap goals and best ideas; cull excess |

### Iteration Decision
At the end of each evaluation:
- **If goals need redefinition, maps are insufficient, or the team feels "lost"** → cycle again with refined scope
- **If confident and enthusiastic about solutions** → move to implementation
- **Minimum 3 cycles**, even in a 1-day session

### Cycle Planning (Fibonacci)
| Cycle | Days | Purpose |
|-------|------|---------|
| 1 | 1 | Reconnaissance — quick survey of entire challenge |
| 2 | 1 | Repeat first cycle for team familiarity |
| 3 | 2 | Deeper analysis, first refined goals |
| 4 | 3 | Detailed mapping, initial solutions |
| 5 | 5 | Refined solutions, draft roadmap |
| 6 | 8 | Robust solutions, formalized roadmap |
| 7 | 13 | Validation, external review |
| 8 | 21 | Final polish, documentation |

---

## Network Parameters Reference

SiD defines three families of network parameters for quantitative system health assessment:

### CRAFTDCCV — Resilience & Structure
| Parameter | Description | Target Direction |
|-----------|-------------|-----------------|
| **Connectivity** | How well linked the network is | Moderate — enough redundancy without chaos |
| **Redundancy** | Degree of overlapping/similar elements | Low–moderate — monoculture is fragile |
| **Awareness** | Visibility and identity of the system to its agents | High |
| **Flexibility** | Capacity to adapt and reconfigure | High |
| **Transparency** | Visibility of information, decisions, and processes | High |
| **Diversity** | Variety of elements, functions, and connections | Maximize — major driver of resilience |
| **Complexity** | Level of structural intricacy | Moderate — enough richness, not chaos |
| **Centrality** | Degree of centralization vs. distribution | Monitor — high centrality = single points of failure |
| **Variety** | Range of different types in each category | Maximize |

### PEAIE — Performance & Adaptation
| Parameter | Description | Target Direction |
|-----------|-------------|-----------------|
| **Productivity** | Output per unit input | Optimize for context |
| **Efficiency** | Ratio of useful output to total input | Maximize |
| **Autonomy** | Self-sufficiency; independence from external inputs | Maximize (within system boundaries) |
| **Integrity** | Wholeness; coherence of system identity and function | Maintain |
| **Emergence** | Novel properties arising from interactions that parts alone don't have | Cultivate |

### SSCNE — System Dynamics
| Parameter | Description | Target Direction |
|-----------|-------------|-----------------|
| **Synergy** | Combined effect greater than sum of parts | Maximize |
| **Self-organization** | Capacity to spontaneously form order | Cultivate |
| **Synchronicity** | Temporal coordination between elements | Optimize |
| **Nestedness** | Hierarchical containment (systems within systems) | Maintain |
| **Evolution** | Capacity for adaptive change over time | Enable |

### For Syntropic Agroforestry Simulator
| SiD Parameter | Syntropy Mapping |
|---------------|-----------------|
| **Circularity / Autonomy** | Biomass surplus ratio; closed nutrient loops |
| **Diversity** | Strata occupation; species count per stratum; Shannon index |
| **Resilience** | Successional redundancy; species ready to replace senescing ones |
| **Connectivity** | Nutrient travel distance (A-row → decomposition → C-row uptake) |
| **Synergy** | Companion planting benefits; guild interactions |
| **Nestedness** | Strata structure; succession phases nested within overall system |
| **Self-organization** | Natural regeneration; emergent species establishment |

---

## Integration: SiD + Syntropy

When SiD is applied to Syntropic Agroforestry design:

| SiD Step | Syntropy Application |
|----------|---------------------|
| **Goal Setting** | System-wide performative goals: "closed-loop biomass cycling", "complete strata occupation", "positive soil carbon trajectory" |
| **System Mapping** | Spatial graph of A-rows, C-rows, species as nodes; biomass flows, nutrient transfers, shading interactions as edges; time maps of succession stages |
| **System Understanding** | Immerse in the land; walk the rows; observe emergence and self-organization patterns; develop intuition for metabolic health |
| **Solutioning** | Block strategy: align species choices with successional group needs; identify leverage points (strata gaps, nutrient bottlenecks) |
| **Roadmapping** | Phased planting: Placenta phase → Secondary I → Secondary II → Primary maturation. Each phase triggered by metabolic health checks. |
| **Evaluation** | KPI tracking: biomass surplus, species diversity trends, soil organic carbon trajectory. Iterate planting density and species selection. |

---

## References

- Except Integrated Sustainability. (2019). *SiD: Symbiosis in Development — Systemic Design Framework* (v4.6.8). Amsterdam.
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green Publishing.
- Barabási, A.-L. (2016). *Network Science*. Cambridge University Press.
- Walker, B., & Salt, D. (2006). *Resilience Thinking*. Island Press.
- Beer, S. (1972). *Brain of the Firm*. (Viable Systems Model).
