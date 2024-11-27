from enum import Enum


class Filledness(str, Enum):
    linear = "linear"
    filled = "filled"


class Connector(str, Enum):
    straight = "straight"
    curved = "curved"
    twoline = "twoline"


class TilingColor(Enum):
    base = 0
    inverted = 1


class HybridFill(Enum):
    none = 0
    hybrid_1 = 1
    hybrid_2 = 2


class AnimationMethod(str, Enum):
    # Defines how to rotate tiles from previous grid state
    # Previous grid state defaults to all zeros, but can be the grid of another tiling
    at_once = "at_once"  # Rotate all necessary tiles at once
    by_tile = "by_tile"  # Rotate tiles in order from top-left to bottom right
    by_ring = "by_ring"  # Rotate tiles in ring form starting from the center


class HexTop(str, Enum):
    pointy = "pointy"
    flat = "flat"
