from dataclasses import dataclass
from decimal import Decimal

from domain.entities.enums import NodeType, Boundary, Dimension, EdgeType, Nonlinearity


@dataclass
class SystemNode:
    id: str
    name: str
    node_type: NodeType
    dimension: Dimension
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
