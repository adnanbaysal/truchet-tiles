from enum import Enum
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


class RectGridGenerator:
    def __init__(
        self, grid_size: int, grid_type: RectGridType = RectGridType.XOR
    ) -> None:
        self._grid_size = grid_size
        self._grid_type = grid_type
        self._grid_types = list(RectGridType)
        self._grid_type_index = self._grid_types.index(self._grid_type)
        self._grid: list[list[int]] = []

    def get_grid_type(self) -> RectGridType:
        return self._grid_type

    @property
    def grid(self) -> list[list[int]]:
        if not self._grid:
            self._generate_grid()

        return self._grid

    def _generate_grid(self):
        match self._grid_type:
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

        self._grid = [
            [grid_func(x, y) for x in range(self._grid_size)]
            for y in range(self._grid_size)
        ]

    def get_next_grid(self) -> list[list[int]]:
        self._grid_type_index = (self._grid_type_index + 1) % len(self._grid_types)
        self._grid_type = self._grid_types[self._grid_type_index]
        self._generate_grid()
        return self._grid

    def get_prev_grid(self) -> list[list[int]]:
        self._grid_type_index = (self._grid_type_index - 1) % len(self._grid_types)
        self._grid_type = self._grid_types[self._grid_type_index]
        self._generate_grid()
        return self._grid

    def get_grid_by_name(self, name: str) -> list[list[int]]:
        self._grid_type = RectGridType(name)
        self._generate_grid()
        return self._grid
