from enum import Enum
from functools import cache
from random import randint

from truchet_tiles.common.math import parity


class RectGridType(str, Enum):
    XOR = "xor"
    MULTXOR = "multxor"
    POWXOR = "powxor"
    SUMXOR = "sumxor"
    SYMPOWSUMXOR = "sympowsumxor"
    ANDXOR = "andxor"
    ORXOR = "orxor"
    MOD = "mod"
    RANDOM = "random"
    THUESHIFT = "thueshift"
    ZEROS = "zeros"
    ONES = "ones"


@cache
def get_rect_grid(grid_size: int, grid_type: RectGridType) -> list[list[int]]:
    match grid_type:
        case RectGridType.XOR:
            grid_func = lambda x, y: parity(x ^ y)  # noqa: E731
        case RectGridType.MULTXOR:
            grid_func = lambda x, y: parity(x * y)  # noqa: E731
        case RectGridType.POWXOR:
            grid_func = lambda x, y: parity(x**y)  # noqa: E731
        case RectGridType.SUMXOR:
            grid_func = lambda x, y: parity(x + y)  # noqa: E731
        case RectGridType.SYMPOWSUMXOR:
            grid_func = lambda x, y: parity(x**y + y**x)  # noqa: E731
        case RectGridType.ANDXOR:
            grid_func = lambda x, y: parity(x & y)  # noqa: E731
        case RectGridType.ORXOR:
            grid_func = lambda x, y: parity(x | y)  # noqa: E731
        case RectGridType.MOD:
            grid_func = lambda x, y: 0 if (y + 1) % (x + 1) == 0 else 1  # noqa: E731
        case RectGridType.THUESHIFT:
            grid_func = lambda x, y: parity(x) ^ parity(x + y)  # noqa: E731
        case RectGridType.ZEROS:
            grid_func = lambda x, y: 0  # noqa: E731
        case RectGridType.ONES:
            grid_func = lambda x, y: 1  # noqa: E731
        case _:
            grid_func = lambda x, y: randint(0, 1)  # noqa: E731

    return [[grid_func(x, y) for x in range(grid_size)] for y in range(grid_size)]
