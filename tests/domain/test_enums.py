import pytest
from decimal import Decimal
from domain.entities.enums import (
    Stratum, SuccessionStage, LightRequirement, RowType,
    Dimension, NodeType, EdgeType, Nonlinearity, Boundary,
    WaterRequirement, PruningRegime,
)


class TestEnums:
    def test_stratum_values(self):
        assert Stratum.EMERGENT.value == "EMERGENT"
        assert Stratum.HIGH.value == "HIGH"
        assert len(Stratum) == 5

    def test_succession_stages(self):
        assert SuccessionStage.PLACENTA.value == "PLACENTA"
        assert SuccessionStage.PRIMARY.value == "PRIMARY"
        assert len(SuccessionStage) == 4

    def test_light_requirement(self):
        assert LightRequirement.SCIOPHYTE.value == "SCIOPHYTE"

    def test_row_types(self):
        assert RowType.A.value == "A"
        assert RowType.C.value == "C"

    def test_pruning_regimes(self):
        assert PruningRegime.AGGRESSIVE.value == "AGGRESSIVE"
        assert PruningRegime.NONE.value == "NONE"
