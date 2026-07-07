import pytest
from decimal import Decimal
from domain.entities.system_map import SystemNode, SystemEdge
from domain.entities.enums import (
    NodeType, EdgeType, Boundary, Dimension, Nonlinearity,
)


class TestSystemNode:
    def test_create_node(self):
        node = SystemNode(
            id="N-001",
            name="Soil Organic Carbon",
            node_type=NodeType.STOCK,
            dimension=Dimension.ECOLOGICAL,
            boundary=Boundary.INTERNAL,
            initial_value=Decimal("50"),
            unit="tons/ha",
            resilience=Decimal("0.7"),
            description="Soil organic carbon stock in top 30cm",
        )
        assert node.name == "Soil Organic Carbon"
        assert node.node_type == NodeType.STOCK
        assert node.initial_value == Decimal("50")
        assert node.resilience == Decimal("0.7")


class TestSystemEdge:
    def test_create_edge(self):
        edge = SystemEdge(
            id="E-001",
            source_node_id="N-001",
            target_node_id="N-002",
            edge_type=EdgeType.CAUSAL_POSITIVE,
            strength=Decimal("0.8"),
            delay_months=3,
            nonlinearity=Nonlinearity.LINEAR,
            description="Higher soil carbon increases water retention",
        )
        assert edge.source_node_id == "N-001"
        assert edge.strength == Decimal("0.8")

    def test_edge_strength_bounds(self):
        with pytest.raises(ValueError, match="between -1 and 1"):
            SystemEdge(
                id="E-002",
                source_node_id="N-001",
                target_node_id="N-002",
                edge_type=EdgeType.CAUSAL_POSITIVE,
                strength=Decimal("1.5"),
            )

    def test_edge_negative_strength(self):
        edge = SystemEdge(
            id="E-003",
            source_node_id="N-001",
            target_node_id="N-002",
            edge_type=EdgeType.CAUSAL_NEGATIVE,
            strength=Decimal("-0.5"),
        )
        assert edge.strength == Decimal("-0.5")

    def test_edge_defaults(self):
        edge = SystemEdge(
            id="E-004",
            source_node_id="N-001",
            target_node_id="N-002",
            edge_type=EdgeType.MATERIAL_FLOW,
            strength=Decimal("0.3"),
        )
        assert edge.delay_months == 0
        assert edge.nonlinearity == Nonlinearity.LINEAR
        assert edge.description == ""
