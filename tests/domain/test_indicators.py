import pytest
from decimal import Decimal
from domain.value_objects.indicators import HealthIndicators, NetworkParameters


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


class TestNetworkParameters:
    def test_healthy_network(self):
        np = NetworkParameters(
            connectance=Decimal("0.2"),
            modularity=Decimal("0.5"),
            reinforcing_loops=3,
            balancing_loops=3,
            resilience_index=Decimal("0.7"),
            circularity=Decimal("0.85"),
            diversity_shannon_index=Decimal("2.5"),
            average_path_length=Decimal("4"),
            synergy_density=Decimal("0.6"),
            leverage_potential=Decimal("0.5"),
        )
        assert np.is_healthy
        assert np.feedback_loop_ratio == Decimal("1.0")

    def test_unhealthy_network(self):
        np = NetworkParameters(
            connectance=Decimal("0.5"),
            modularity=Decimal("0.1"),
            reinforcing_loops=5,
            balancing_loops=1,
            resilience_index=Decimal("0.3"),
            circularity=Decimal("0.4"),
            diversity_shannon_index=Decimal("1.0"),
            average_path_length=Decimal("8"),
            synergy_density=Decimal("0.2"),
            leverage_potential=Decimal("0.1"),
        )
        assert not np.is_healthy

    def test_feedback_loop_ratio_no_balancing(self):
        np = NetworkParameters(
            connectance=Decimal("0.2"),
            modularity=Decimal("0.5"),
            reinforcing_loops=5,
            balancing_loops=0,
            resilience_index=Decimal("0.7"),
            circularity=Decimal("0.9"),
            diversity_shannon_index=Decimal("2.0"),
            average_path_length=Decimal("3"),
            synergy_density=Decimal("0.5"),
            leverage_potential=Decimal("0.5"),
        )
        assert np.feedback_loop_ratio == Decimal("Infinity")
