import pytest
from decimal import Decimal
from domain.entities.system_map import SystemNode, SystemEdge, SystemMap
from domain.entities.enums import (
    NodeType, EdgeType, Boundary, ELSICategory, SnoLevel, Nonlinearity,
    MapDimension, MapScale,
)


class TestSystemNode:
    def test_create_node(self):
        node = SystemNode(
            id="N-001",
            name="Soil Organic Carbon",
            node_type=NodeType.STOCK,
            elsi_category=ELSICategory.ECOSYSTEMS,
            scope=SnoLevel.OBJECT,
            boundary=Boundary.INTERNAL,
            initial_value=Decimal("50"),
            unit="tons/ha",
            resilience=Decimal("0.7"),
            description="Soil organic carbon stock in top 30cm",
        )
        assert node.name == "Soil Organic Carbon"
        assert node.node_type == NodeType.STOCK
        assert node.elsi_category == ELSICategory.ECOSYSTEMS
        assert node.scope == SnoLevel.OBJECT
        assert node.initial_value == Decimal("50")
        assert node.resilience == Decimal("0.7")

    def test_node_elsi_energy(self):
        node = SystemNode(
            id="N-002",
            name="Solar Input",
            node_type=NodeType.FLOW,
            elsi_category=ELSICategory.ENERGY,
            scope=SnoLevel.SYSTEM,
            boundary=Boundary.EXTERNAL,
        )
        assert node.elsi_category == ELSICategory.ENERGY


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


class TestSystemMap:
    def test_create_map(self):
        node = SystemNode(
            id="N-001",
            name="Soil Carbon",
            node_type=NodeType.STOCK,
            elsi_category=ELSICategory.ECOSYSTEMS,
            scope=SnoLevel.OBJECT,
            boundary=Boundary.INTERNAL,
        )
        edge = SystemEdge(
            id="E-001",
            source_node_id="N-001",
            target_node_id="N-002",
            edge_type=EdgeType.CAUSAL_POSITIVE,
            strength=Decimal("0.8"),
        )
        smap = SystemMap(
            id="SM-001",
            name="Soil Carbon Map",
            map_dimension=MapDimension.CONTEXT,
            map_scale=MapScale.MEDIUM,
            nodes=[node],
            edges=[edge],
        )
        assert len(smap.nodes) == 1
        assert len(smap.edges) == 1

    def test_add_node(self):
        smap = SystemMap(
            id="SM-002",
            name="Test Map",
            map_dimension=MapDimension.SPACE,
            map_scale=MapScale.SMALL,
        )
        node = SystemNode(
            id="N-001",
            name="Test",
            node_type=NodeType.ACTOR,
            elsi_category=ELSICategory.CULTURE,
            scope=SnoLevel.NETWORK,
            boundary=Boundary.INTERNAL,
        )
        smap.add_node(node)
        assert len(smap.nodes) == 1

    def test_add_edge(self):
        smap = SystemMap(
            id="SM-003",
            name="Test Map",
            map_dimension=MapDimension.TIME,
            map_scale=MapScale.LARGE,
        )
        edge = SystemEdge(
            id="E-001",
            source_node_id="A",
            target_node_id="B",
            edge_type=EdgeType.INFORMATION_FLOW,
            strength=Decimal("0.5"),
        )
        smap.add_edge(edge)
        assert len(smap.edges) == 1

    def test_get_feedback_loops_reinforcing(self):
        smap = SystemMap(
            id="SM-004",
            name="Reinforcing loop",
            map_dimension=MapDimension.CONTEXT,
            map_scale=MapScale.SMALL,
        )
        n1 = SystemNode(
            id="A", name="A", node_type=NodeType.STOCK,
            elsi_category=ELSICategory.ECOSYSTEMS, scope=SnoLevel.OBJECT,
            boundary=Boundary.INTERNAL,
        )
        n2 = SystemNode(
            id="B", name="B", node_type=NodeType.STOCK,
            elsi_category=ELSICategory.ECOSYSTEMS, scope=SnoLevel.OBJECT,
            boundary=Boundary.INTERNAL,
        )
        e1 = SystemEdge(id="E1", source_node_id="A", target_node_id="B",
                         edge_type=EdgeType.CAUSAL_POSITIVE, strength=Decimal("1"))
        e2 = SystemEdge(id="E2", source_node_id="B", target_node_id="A",
                         edge_type=EdgeType.CAUSAL_POSITIVE, strength=Decimal("1"))
        smap.add_node(n1)
        smap.add_node(n2)
        smap.add_edge(e1)
        smap.add_edge(e2)
        reinforcing, balancing = smap.get_feedback_loops()
        assert len(reinforcing) >= 1

    def test_empty_map(self):
        smap = SystemMap(
            id="SM-005",
            name="Empty",
            map_dimension=MapDimension.CONTEXT,
            map_scale=MapScale.SMALL,
        )
        assert len(smap.nodes) == 0
        assert len(smap.edges) == 0
