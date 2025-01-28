from collections import defaultdict
from enum import Enum
from functools import cache
from random import randint

from truchet_tiles.common.math import parity
from truchet_tiles.common.number_triangle import (
    get_baysal_triangle,
    get_hosoya_triangle,
    get_pascal_triangle,
)
from truchet_tiles.rectangular.grid.triangle_converter import (
    triangle_to_reflected_square,
    triangle_to_subsquare,
)


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
    PASCALSUBXOR = "pascalsubxor"
    PASCALSUBMOD = "pascalsubmod"
    PASCALREFXOR = "pascalrefxor"
    PASCALREFMOD = "pascalrefmod"
    BAYSALSUBXOR = "baysalsubxor"
    BAYSALSUBMOD = "baysalsubmod"
    BAYSALREFXOR = "baysalrefxor"
    BAYSALREFMOD = "baysalrefmod"
    HOSOYASUBXOR = "hosoyasubxor"
    HOSOYASUBMOD = "hosoyasubmod"
    HOSOYAREFXOR = "hosoyarefxor"
    HOSOYAREFMOD = "hosoyarefmod"


@cache
def baysal_reflected_square(grid_size: int) -> defaultdict[tuple[int, int], int]:
    return triangle_to_reflected_square(get_baysal_triangle(grid_size))


@cache
def baysal_subsquare(grid_size: int) -> defaultdict[tuple[int, int], int]:
    return triangle_to_subsquare(get_baysal_triangle(2 * grid_size))


@cache
def hosoya_reflected_square(grid_size: int) -> defaultdict[tuple[int, int], int]:
    return triangle_to_reflected_square(get_hosoya_triangle(grid_size))


@cache
def hosoya_subsquare(grid_size: int) -> defaultdict[tuple[int, int], int]:
    return triangle_to_subsquare(get_hosoya_triangle(2 * grid_size))


@cache
def pascal_reflected_square(grid_size: int) -> defaultdict[tuple[int, int], int]:
    return triangle_to_reflected_square(get_pascal_triangle(grid_size))


@cache
def pascal_subsquare(grid_size: int) -> defaultdict[tuple[int, int], int]:
    return triangle_to_subsquare(get_pascal_triangle(2 * grid_size))


@cache
def get_rect_grid(
    grid_size: int, grid_type: RectGridType
) -> defaultdict[tuple[int, int], int]:
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
        case RectGridType.PASCALSUBXOR:
            grid_func = lambda x, y: parity(pascal_subsquare(grid_size)[(x, y)])  # noqa: E731
        case RectGridType.PASCALSUBMOD:
            grid_func = lambda x, y: pascal_subsquare(grid_size)[(x, y)] % 2  # noqa: E731
        case RectGridType.PASCALREFXOR:
            grid_func = lambda x, y: parity(pascal_reflected_square(grid_size)[(x, y)])  # noqa: E731
        case RectGridType.PASCALREFMOD:
            grid_func = lambda x, y: pascal_reflected_square(grid_size)[(x, y)] % 2  # noqa: E731
        case RectGridType.BAYSALSUBXOR:
            grid_func = lambda x, y: parity(baysal_subsquare(grid_size)[(x, y)])  # noqa: E731
        case RectGridType.BAYSALSUBMOD:
            grid_func = lambda x, y: baysal_subsquare(grid_size)[(x, y)] % 2  # noqa: E731
        case RectGridType.BAYSALREFXOR:
            grid_func = lambda x, y: parity(baysal_reflected_square(grid_size)[(x, y)])  # noqa: E731
        case RectGridType.BAYSALREFMOD:
            grid_func = lambda x, y: baysal_reflected_square(grid_size)[(x, y)] % 2  # noqa: E731
        case RectGridType.HOSOYASUBXOR:
            grid_func = lambda x, y: parity(hosoya_subsquare(grid_size)[(x, y)])  # noqa: E731
        case RectGridType.HOSOYASUBMOD:
            grid_func = lambda x, y: hosoya_subsquare(grid_size)[(x, y)] % 2  # noqa: E731
        case RectGridType.HOSOYAREFXOR:
            grid_func = lambda x, y: parity(hosoya_reflected_square(grid_size)[(x, y)])  # noqa: E731
        case RectGridType.HOSOYAREFMOD:
            grid_func = lambda x, y: hosoya_reflected_square(grid_size)[(x, y)] % 2  # noqa: E731
        case _:
            grid_func = lambda x, y: randint(0, 1)  # noqa: E731

    return defaultdict(
        int,
        (((x, y), grid_func(x, y)) for x in range(grid_size) for y in range(grid_size)),
    )
