from enum import Enum


class Connector(str, Enum):
    twoline = "twoline"
    curved = "curved"
    line = "line"


class HybridFill(Enum):
    none = 0
    hybrid_1 = 1
    hybrid_2 = 2


class SvgColors:
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    RED = "#FF0000"
