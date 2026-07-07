import pytest
from decimal import Decimal
from domain.entities.enums import (
    Stratum, SuccessionStage, LightRequirement, RowType,
    SnoLevel, ELSICategory, MapDimension, MapScale,
    TransitionType, ActionType, NodeType, EdgeType,
    Nonlinearity, Boundary, WaterRequirement, PruningRegime,
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


class TestSNOLevel:
    def test_sno_levels(self):
        assert SnoLevel.SYSTEM.value == "SYSTEM"
        assert SnoLevel.NETWORK.value == "NETWORK"
        assert SnoLevel.OBJECT.value == "OBJECT"
        assert len(SnoLevel) == 3


class TestELSIcategory:
    def test_elsi_categories(self):
        assert ELSICategory.ENERGY.value == "ENERGY"
        assert ELSICategory.ECONOMY.value == "ECONOMY"
        assert ELSICategory.HAPPINESS.value == "HAPPINESS"
        assert len(ELSICategory) == 8


class TestMapDimensions:
    def test_map_dimensions(self):
        assert MapDimension.TIME.value == "TIME"
        assert MapDimension.SPACE.value == "SPACE"
        assert MapDimension.CONTEXT.value == "CONTEXT"
        assert len(MapDimension) == 3

    def test_map_scales(self):
        assert MapScale.SMALL.value == "SMALL"
        assert MapScale.MEDIUM.value == "MEDIUM"
        assert MapScale.LARGE.value == "LARGE"
        assert len(MapScale) == 3


class TestTransitionType:
    def test_transition_types(self):
        assert TransitionType.START.value == "START"
        assert TransitionType.STOP.value == "STOP"
        assert TransitionType.CHANGE.value == "CHANGE"
        assert TransitionType.ENABLE.value == "ENABLE"
        assert TransitionType.GOVERN.value == "GOVERN"
        assert len(TransitionType) == 5


class TestActionType:
    def test_action_types(self):
        assert ActionType.PUSH.value == "PUSH"
        assert ActionType.PULL.value == "PULL"
        assert ActionType.LUBRICATE.value == "LUBRICATE"
        assert ActionType.SYSTEMIC.value == "SYSTEMIC"
        assert len(ActionType) == 4
