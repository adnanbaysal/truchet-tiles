from enum import Enum


class Connector(str, Enum):
    twoline = "twoline"
    curved = "curved"
    line = "line"


class SvgColors:
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    RED = "#FF0000"
