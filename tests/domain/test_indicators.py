import pytest
from decimal import Decimal
from domain.value_objects.indicators import (
    HealthIndicators, NetworkParameters,
    CraftdccvParameters, PeaieParameters, SscneParameters,
)


class TestHealthIndicators:
    def test_metabolic_healthy(self):
        h = HealthIndicators(
            surplus_ratio=Decimal("1.3"),
            mulch_coverage_ratio=Decimal("1.2"),
            soil_carbon_trend=Decimal("0.1"),
            diversity_shannon_index=Decimal("2.5"),
            circularity=Decimal("0.9"),
            resilience_index=Decimal("0.7"),
        )
        assert h.is_metabolic_healthy
        assert h.is_soil_healthy
        assert h.is_system_healthy

    def test_metabolic_unhealthy_surplus(self):
        h = HealthIndicators(
            surplus_ratio=Decimal("0.9"),
            mulch_coverage_ratio=Decimal("1.0"),
            soil_carbon_trend=Decimal("0.1"),
            diversity_shannon_index=Decimal("2.0"),
            circularity=Decimal("0.5"),
            resilience_index=Decimal("0.5"),
        )
        assert not h.is_metabolic_healthy

    def test_soil_unhealthy(self):
        h = HealthIndicators(
            surplus_ratio=Decimal("1.5"),
            mulch_coverage_ratio=Decimal("1.5"),
            soil_carbon_trend=Decimal("-0.1"),
            diversity_shannon_index=Decimal("2.0"),
            circularity=Decimal("0.5"),
            resilience_index=Decimal("0.5"),
        )
        assert not h.is_soil_healthy


class TestCraftdccvParameters:
    def test_healthy(self):
        p = CraftdccvParameters(
            connectivity=Decimal("0.3"),
            redundancy=Decimal("0.4"),
            awareness=Decimal("0.8"),
            flexibility=Decimal("0.7"),
            transparency=Decimal("0.9"),
            diversity=Decimal("0.8"),
            complexity=Decimal("0.4"),
            centrality=Decimal("0.2"),
            variety=Decimal("0.7"),
        )
        assert p.is_healthy
        assert p.resilience_score >= Decimal("0.6")

    def test_unhealthy(self):
        p = CraftdccvParameters(
            connectivity=Decimal("0.1"),
            redundancy=Decimal("0.1"),
            awareness=Decimal("0.2"),
            flexibility=Decimal("0.2"),
            transparency=Decimal("0.2"),
            diversity=Decimal("0.1"),
            complexity=Decimal("0.9"),
            centrality=Decimal("0.9"),
            variety=Decimal("0.1"),
        )
        assert not p.is_healthy

    def test_immutability(self):
        p = CraftdccvParameters(
            connectivity=Decimal("0.3"), redundancy=Decimal("0.4"),
            awareness=Decimal("0.8"), flexibility=Decimal("0.7"),
            transparency=Decimal("0.9"), diversity=Decimal("0.8"),
            complexity=Decimal("0.4"), centrality=Decimal("0.2"),
            variety=Decimal("0.7"),
        )
        with pytest.raises(AttributeError):
            p.connectivity = Decimal("0.5")


class TestPeaieParameters:
    def test_healthy(self):
        p = PeaieParameters(
            productivity=Decimal("0.8"),
            efficiency=Decimal("0.85"),
            autonomy=Decimal("0.7"),
            integrity=Decimal("0.9"),
            emergence=Decimal("0.6"),
        )
        assert p.is_healthy

    def test_unhealthy(self):
        p = PeaieParameters(
            productivity=Decimal("0.3"),
            efficiency=Decimal("0.3"),
            autonomy=Decimal("0.2"),
            integrity=Decimal("0.4"),
            emergence=Decimal("0.1"),
        )
        assert not p.is_healthy


class TestSscneParameters:
    def test_healthy(self):
        p = SscneParameters(
            synergy=Decimal("0.8"),
            self_organization=Decimal("0.7"),
            synchronicity=Decimal("0.6"),
            nestedness=Decimal("0.85"),
            evolution=Decimal("0.7"),
        )
        assert p.is_healthy

    def test_unhealthy(self):
        p = SscneParameters(
            synergy=Decimal("0.3"),
            self_organization=Decimal("0.2"),
            synchronicity=Decimal("0.1"),
            nestedness=Decimal("0.3"),
            evolution=Decimal("0.2"),
        )
        assert not p.is_healthy


class TestNetworkParameters:
    def test_healthy_network(self):
        np = NetworkParameters(
            craftdccv=CraftdccvParameters(
                connectivity=Decimal("0.2"), redundancy=Decimal("0.5"),
                awareness=Decimal("0.8"), flexibility=Decimal("0.7"),
                transparency=Decimal("0.9"), diversity=Decimal("0.8"),
                complexity=Decimal("0.4"), centrality=Decimal("0.3"),
                variety=Decimal("0.7"),
            ),
            peaie=PeaieParameters(
                productivity=Decimal("0.8"), efficiency=Decimal("0.85"),
                autonomy=Decimal("0.7"), integrity=Decimal("0.9"),
                emergence=Decimal("0.6"),
            ),
            sscne=SscneParameters(
                synergy=Decimal("0.8"), self_organization=Decimal("0.7"),
                synchronicity=Decimal("0.6"), nestedness=Decimal("0.85"),
                evolution=Decimal("0.7"),
            ),
            reinforcing_loops=3,
            balancing_loops=3,
        )
        assert np.is_healthy
        assert np.feedback_loop_ratio == Decimal("1.0")
        assert np.aggregate_score >= Decimal("0.6")

    def test_unhealthy_network(self):
        np = NetworkParameters(
            craftdccv=CraftdccvParameters(
                connectivity=Decimal("0.1"), redundancy=Decimal("0.1"),
                awareness=Decimal("0.2"), flexibility=Decimal("0.2"),
                transparency=Decimal("0.2"), diversity=Decimal("0.1"),
                complexity=Decimal("0.9"), centrality=Decimal("0.9"),
                variety=Decimal("0.1"),
            ),
            peaie=PeaieParameters(
                productivity=Decimal("0.3"), efficiency=Decimal("0.3"),
                autonomy=Decimal("0.2"), integrity=Decimal("0.4"),
                emergence=Decimal("0.1"),
            ),
            sscne=SscneParameters(
                synergy=Decimal("0.2"), self_organization=Decimal("0.2"),
                synchronicity=Decimal("0.1"), nestedness=Decimal("0.3"),
                evolution=Decimal("0.2"),
            ),
            reinforcing_loops=5,
            balancing_loops=1,
        )
        assert not np.is_healthy

    def test_feedback_loop_ratio_no_balancing(self):
        np = NetworkParameters(
            craftdccv=CraftdccvParameters(
                connectivity=Decimal("0.2"), redundancy=Decimal("0.5"),
                awareness=Decimal("0.8"), flexibility=Decimal("0.7"),
                transparency=Decimal("0.9"), diversity=Decimal("0.8"),
                complexity=Decimal("0.4"), centrality=Decimal("0.3"),
                variety=Decimal("0.7"),
            ),
            peaie=PeaieParameters(
                productivity=Decimal("0.8"), efficiency=Decimal("0.85"),
                autonomy=Decimal("0.7"), integrity=Decimal("0.9"),
                emergence=Decimal("0.6"),
            ),
            sscne=SscneParameters(
                synergy=Decimal("0.8"), self_organization=Decimal("0.7"),
                synchronicity=Decimal("0.6"), nestedness=Decimal("0.85"),
                evolution=Decimal("0.7"),
            ),
            reinforcing_loops=5,
            balancing_loops=0,
        )
        assert np.feedback_loop_ratio == Decimal("Infinity")
