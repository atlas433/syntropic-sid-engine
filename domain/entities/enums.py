from enum import Enum


class Stratum(Enum):
    EMERGENT = "EMERGENT"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    GROUND_COVER = "GROUND_COVER"


class SuccessionStage(Enum):
    PLACENTA = "PLACENTA"
    SECONDARY_I = "SECONDARY_I"
    SECONDARY_II = "SECONDARY_II"
    PRIMARY = "PRIMARY"


class LightRequirement(Enum):
    HELIOPHILE = "HELIOPHILE"
    INTERMEDIATE = "INTERMEDIATE"
    SCIOPHYTE = "SCIOPHYTE"


class RowType(Enum):
    A = "A"
    C = "C"


class SnoLevel(Enum):
    SYSTEM = "SYSTEM"
    NETWORK = "NETWORK"
    OBJECT = "OBJECT"


class ELSICategory(Enum):
    ENERGY = "ENERGY"
    MATERIALS = "MATERIALS"
    ECOSYSTEMS = "ECOSYSTEMS"
    SPECIES = "SPECIES"
    CULTURE = "CULTURE"
    ECONOMY = "ECONOMY"
    HEALTH = "HEALTH"
    HAPPINESS = "HAPPINESS"


class MapDimension(Enum):
    TIME = "TIME"
    SPACE = "SPACE"
    CONTEXT = "CONTEXT"


class MapScale(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class TransitionType(Enum):
    START = "START"
    STOP = "STOP"
    CHANGE = "CHANGE"
    ENABLE = "ENABLE"
    GOVERN = "GOVERN"


class ActionType(Enum):
    PUSH = "PUSH"
    PULL = "PULL"
    LUBRICATE = "LUBRICATE"
    SYSTEMIC = "SYSTEMIC"


class NodeType(Enum):
    STOCK = "STOCK"
    FLOW = "FLOW"
    ACTOR = "ACTOR"
    CONSTRAINT = "CONSTRAINT"
    LEVERAGE_POINT = "LEVERAGE_POINT"
    EXTERNALITY = "EXTERNALITY"


class EdgeType(Enum):
    CAUSAL_POSITIVE = "CAUSAL_POSITIVE"
    CAUSAL_NEGATIVE = "CAUSAL_NEGATIVE"
    MATERIAL_FLOW = "MATERIAL_FLOW"
    INFORMATION_FLOW = "INFORMATION_FLOW"
    ENERGY_FLOW = "ENERGY_FLOW"
    REGULATORY = "REGULATORY"


class Nonlinearity(Enum):
    LINEAR = "LINEAR"
    THRESHOLD = "THRESHOLD"
    DIMINISHING_RETURNS = "DIMINISHING_RETURNS"
    EXPONENTIAL = "EXPONENTIAL"


class Boundary(Enum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"


class WaterRequirement(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class PruningRegime(Enum):
    AGGRESSIVE = "AGGRESSIVE"
    SELECTIVE = "SELECTIVE"
    FORMATIVE = "FORMATIVE"
    NONE = "NONE"
