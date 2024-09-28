from enum import Enum
from random import randint


class GridType(str, Enum):
    XOR = "xor"
    MULTXOR = "multxor"
    POWXOR = "powxor"
    SUMXOR = "sumxor"
    SYMPOWSUMXOR = "sympowsumxor"
    ANDXOR = "andxor"
    ORXOR = "orxor"
    MOD = "mod"
    RANDOM = "random"


def parity(x):
    par = 0
    while x != 0:
        par ^= x & 1
        x = int(x / 2)
    return par


def generate_grid(grid_size: int, grid_type: GridType) -> list[list[int]]:
    match grid_type:
        case GridType.XOR:
            grid_func = lambda x, y: parity(x ^ y)  # noqa: E731
        case GridType.MULTXOR:
            grid_func = lambda x, y: parity(x * y)  # noqa: E731
        case GridType.POWXOR:
            grid_func = lambda x, y: parity(x**y)  # noqa: E731
        case GridType.SUMXOR:
            grid_func = lambda x, y: parity(x + y)  # noqa: E731
        case GridType.SYMPOWSUMXOR:
            grid_func = lambda x, y: parity(x**y + y**x)  # noqa: E731
        case GridType.ANDXOR:
            grid_func = lambda x, y: parity(x & y)  # noqa: E731
        case GridType.ORXOR:
            grid_func = lambda x, y: parity(x | y)  # noqa: E731
        case GridType.MOD:
            grid_func = lambda x, y: 0 if (y + 1) % (x + 1) == 0 else 1  # noqa: E731
        case _:
            grid_func = lambda x, y: randint(0, 1)  # noqa: E731

    return [[grid_func(x, y) for x in range(grid_size)] for y in range(grid_size)]
