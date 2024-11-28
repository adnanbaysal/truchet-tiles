from enum import Enum


class HexAnimationMethod(str, Enum):
    # Defines how to rotate tiles from previous grid state
    # Previous grid state defaults to all zeros, but can be the grid of another tiling
    at_once = "at_once"  # Rotate all necessary tiles at once
    by_tile = "by_tile"  # Rotate tiles in order from top-left to bottom right
    by_ring = "by_ring"  # Rotate tiles in ring form starting from the center


class HexTop(str, Enum):
    pointy = "pointy"
    flat = "flat"
