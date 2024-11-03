from enum import Enum


class Filledness(str, Enum):
    linear = "linear"
    filled = "filled"


class Curvedness(str, Enum):
    straight = "straight"
    curved = "curved"


class AxisAlignment(str, Enum):
    aligned = "aligned"
    rotated = "rotated"


class TilingColor(int, Enum):
    base = 0
    inverted = 1


class HybridFill(int, Enum):
    none = 0
    hybrid_1 = 1
    hybrid_2 = 2


class Colors:
    SVG_BLACK = "#000000"
    SVG_WHITE = "#FFFFFF"
    SVG_RED = "#FF0000"
    PYG_WHITE = (255, 255, 255)


class AnimationMethod(str, Enum):
    # Defines how to rotate tiles from previous grid state
    # Previous grid state defaults to all zeros, but can be the grid of another tiling
    at_once = "at_once"  # Rotate all necessary tiles at once
    by_tile = "by_tile"  # Rotate tiles in order from top-left to bottom right
    by_row = "by_row"  # Rotate row by row
