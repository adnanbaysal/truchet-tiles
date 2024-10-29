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
