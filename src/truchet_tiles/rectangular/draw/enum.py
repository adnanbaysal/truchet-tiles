from enum import Enum


class AxisAlignment(str, Enum):
    aligned = "aligned"
    rotated = "rotated"


class RectAnimationMethod(str, Enum):
    # Defines how to rotate tiles from previous grid state
    # Previous grid state defaults to all zeros, but can be the grid of another tiling
    at_once = "at_once"  # Rotate all necessary tiles at once
    by_tile = "by_tile"  # Rotate tiles in order from top-left to bottom right
    by_row = "by_row"  # Rotate row by row
