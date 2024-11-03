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


class GridGenerator:
    def __init__(self, grid_size: int, grid_type: GridType = GridType.XOR) -> None:
        self._grid_size = grid_size
        self._grid_type = grid_type
        self._grid_types = list(GridType)
        self._grid_type_index = self._grid_types.index(self._grid_type)

    @staticmethod
    def _parity(x: int) -> int:
        par = 0
        while x != 0:
            par ^= x & 1
            x = int(x / 2)
        return par

    def get_grid_type(self) -> GridType:
        return self._grid_type

    def get_grid(self) -> list[list[int]]:
        match self._grid_type:
            case GridType.XOR:
                grid_func = lambda x, y: self._parity(x ^ y)  # noqa: E731
            case GridType.MULTXOR:
                grid_func = lambda x, y: self._parity(x * y)  # noqa: E731
            case GridType.POWXOR:
                grid_func = lambda x, y: self._parity(x**y)  # noqa: E731
            case GridType.SUMXOR:
                grid_func = lambda x, y: self._parity(x + y)  # noqa: E731
            case GridType.SYMPOWSUMXOR:
                grid_func = lambda x, y: self._parity(x**y + y**x)  # noqa: E731
            case GridType.ANDXOR:
                grid_func = lambda x, y: self._parity(x & y)  # noqa: E731
            case GridType.ORXOR:
                grid_func = lambda x, y: self._parity(x | y)  # noqa: E731
            case GridType.MOD:
                grid_func = lambda x, y: 0 if (y + 1) % (x + 1) == 0 else 1  # noqa: E731
            case _:
                grid_func = lambda x, y: randint(0, 1)  # noqa: E731

        return [
            [grid_func(x, y) for x in range(self._grid_size)]
            for y in range(self._grid_size)
        ]

    def get_next_grid(self) -> list[list[int]]:
        self._grid_type_index = (self._grid_type_index + 1) % len(self._grid_types)
        self._grid_type = self._grid_types[self._grid_type_index]
        return self.get_grid()

    def get_prev_grid(self) -> list[list[int]]:
        self._grid_type_index = (self._grid_type_index - 1) % len(self._grid_types)
        self._grid_type = self._grid_types[self._grid_type_index]
        return self.get_grid()

    def get_grid_by_name(self, name: str) -> list[list[int]]:
        self._grid_type = GridType(name)
        self.get_grid()
