from dataclasses import dataclass
from decimal import Decimal

from domain.entities.enums import (
    NodeType, Boundary, ELSICategory, SnoLevel,
    EdgeType, Nonlinearity, MapDimension, MapScale,
)


@dataclass
class SystemNode:
    id: str
    name: str
    node_type: NodeType
    elsi_category: ELSICategory
    scope: SnoLevel
    boundary: Boundary
    initial_value: Decimal | None = None
    unit: str = ""
    resilience: Decimal = Decimal("0.5")
    description: str = ""


@dataclass
class SystemEdge:
    id: str
    source_node_id: str
    target_node_id: str
    edge_type: EdgeType
    strength: Decimal
    delay_months: int = 0
    nonlinearity: Nonlinearity = Nonlinearity.LINEAR
    description: str = ""

    def __post_init__(self):
        if not Decimal("-1") <= self.strength <= Decimal("1"):
            raise ValueError(f"Edge strength must be between -1 and 1, got {self.strength}")


@dataclass
class SystemMap:
    id: str
    name: str
    map_dimension: MapDimension
    map_scale: MapScale
    nodes: list[SystemNode] = None
    edges: list[SystemEdge] = None
    description: str = ""

    def __post_init__(self):
        if self.nodes is None:
            self.nodes = []
        if self.edges is None:
            self.edges = []

    def add_node(self, node: SystemNode) -> None:
        self.nodes.append(node)

    def add_edge(self, edge: SystemEdge) -> None:
        self.edges.append(edge)

    def get_feedback_loops(self) -> tuple[list[list[str]], list[list[str]]]:
        reinforcing = []
        balancing = []
        adjacency = {}
        for edge in self.edges:
            adjacency.setdefault(edge.source_node_id, []).append(edge)

        for start_node in self.nodes:
            for edge in adjacency.get(start_node.id, []):
                path = [start_node.id, edge.target_node_id]
                loops = self._find_loops(adjacency, start_node.id, edge.target_node_id, path, {edge.target_node_id})
                for loop in loops:
                    product = Decimal("1")
                    for i in range(len(loop) - 1):
                        for e in adjacency.get(loop[i], []):
                            if e.target_node_id == loop[i + 1]:
                                product *= e.strength
                                break
                        else:
                            product = Decimal("0")
                    if product > 0:
                        reinforcing.append(loop)
                    else:
                        balancing.append(loop)

        return reinforcing, balancing

    def _find_loops(self, adjacency, target_id, current_id, path, visited):
        loops = []
        for edge in adjacency.get(current_id, []):
            if edge.target_node_id == target_id:
                loops.append(path + [target_id])
            elif edge.target_node_id not in visited:
                visited.add(edge.target_node_id)
                loops.extend(
                    self._find_loops(adjacency, target_id, edge.target_node_id, path + [edge.target_node_id], visited.copy())
                )
        return loops
