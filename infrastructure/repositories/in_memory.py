from domain.entities.plant import Plant
from domain.entities.row import Row
from domain.entities.enums import RowType
from domain.entities.performative_goal import PerformativeGoal
from domain.entities.system_map import SystemNode, SystemEdge, SystemMap
from domain.entities.roadmap import TransitionRoadmap
from domain.entities.cycle import SiDCycle
from domain.entities.enums import SnoLevel


class InMemoryRowRepository:
    def __init__(self):
        self._rows: dict[str, Row] = {}

    def find_all(self) -> list[Row]:
        return list(self._rows.values())

    def find_by_type(self, row_type: RowType) -> list[Row]:
        return [r for r in self._rows.values() if r.row_type == row_type]

    def save(self, row: Row) -> None:
        self._rows[row.id] = row

    def find_by_id(self, row_id: str) -> Row | None:
        return self._rows.get(row_id)


class InMemoryPlantRepository:
    def __init__(self):
        self._plants: dict[str, Plant] = {}

    def find_by_row(self, row_id: str) -> list[Plant]:
        return [p for p in self._plants.values()]

    def save(self, plant: Plant) -> None:
        self._plants[str(plant.id)] = plant


class InMemoryGoalRepository:
    def __init__(self):
        self._goals: dict[str, PerformativeGoal] = {}

    def find_all(self) -> list[PerformativeGoal]:
        return list(self._goals.values())

    def find_by_id(self, goal_id: str) -> PerformativeGoal | None:
        return self._goals.get(goal_id)

    def find_by_level(self, level: SnoLevel) -> list[PerformativeGoal]:
        return [g for g in self._goals.values() if g.level == level]

    def save(self, goal: PerformativeGoal) -> None:
        self._goals[goal.id] = goal


class InMemorySystemMapRepository:
    def __init__(self):
        self._maps: dict[str, SystemMap] = {}
        self._nodes: dict[str, SystemNode] = {}
        self._edges: dict[str, SystemEdge] = {}

    def find_all_maps(self) -> list[SystemMap]:
        return list(self._maps.values())

    def find_map_by_id(self, map_id: str) -> SystemMap | None:
        return self._maps.get(map_id)

    def find_all_nodes(self) -> list[SystemNode]:
        return list(self._nodes.values())

    def find_all_edges(self) -> list[SystemEdge]:
        return list(self._edges.values())

    def save_map(self, system_map: SystemMap) -> None:
        self._maps[system_map.id] = system_map

    def save_node(self, node: SystemNode) -> None:
        self._nodes[node.id] = node

    def save_edge(self, edge: SystemEdge) -> None:
        self._edges[edge.id] = edge


class InMemoryRoadmapRepository:
    def __init__(self):
        self._roadmaps: dict[str, TransitionRoadmap] = {}

    def find_by_id(self, roadmap_id: str) -> TransitionRoadmap | None:
        return self._roadmaps.get(roadmap_id)

    def save(self, roadmap: TransitionRoadmap) -> None:
        self._roadmaps[roadmap.id] = roadmap


class InMemoryCycleRepository:
    def __init__(self):
        self._cycles: dict[int, SiDCycle] = {}

    def find_all(self) -> list[SiDCycle]:
        return list(self._cycles.values())

    def find_by_cycle_number(self, cycle_number: int) -> SiDCycle | None:
        return self._cycles.get(cycle_number)

    def save(self, cycle: SiDCycle) -> None:
        self._cycles[cycle.cycle_number] = cycle
