from enum import Enum
from random import randint
from typing import Callable

from truchet_tiles.util import parity


class HexGridType(str, Enum):
    # values starting with X means XOR of ... The rest is for how to interpret negative numbers
    # see: https://en.wikipedia.org/wiki/Signed_number_representations
    XSIGNMAG = "xsignmag"  # Negative numbers are represented as sign magnitude form
    XONESCOMP = "xonescomp"  # Negative numbers are represented as one's complement form
    XTWOSCOMP = "xtwoscomp"  # Negative numbers are represented as two's complement form
    XSIGNMAGQR = "xsignmagqr"  # Like xsignmag, but only q and r coordinates are used
    XONESCOMPQR = "xonescompqr"  # Like xonescomp, but only q and r coordinates are used
    XTWOSCOMPQR = "xtwoscompqr"  # Like xtwoscomp, but only q and r coordinates are used
    RANDOM = "random"


def parity_if_positive(func: Callable) -> Callable:
    def decorated(x: int):
        return parity(x) if x >= 0 else func(x)

    return decorated


@parity_if_positive
def sm_parity(x: int) -> int:  # parity for signed magnitude (sm) form
    return 1 ^ parity(-x)


@parity_if_positive
def oc_parity(x: int) -> int:  # parity for ones copmlement (oc) form
    return parity(-x)


@parity_if_positive
def tc_parity(x: int) -> int:  # parity for twos copmlement (tc) form
    return parity(-x + 1)


class HexGridGenerator:
    def __init__(
        self, grid_dimension: int, grid_type: HexGridType = HexGridType.XSIGNMAG
    ) -> None:
        self._grid_dimension = grid_dimension  # radius of the tiling in terms of the number of tile lengths from center
        self._grid_type = grid_type
        self._grid_types = list(HexGridType)
        self._grid_type_index = self._grid_types.index(self._grid_type)
        self._grid: dict[tuple[int, int], int] = {}

    @property
    def grid(self) -> dict[tuple[int, int], int]:
        if not self._grid:
            self._generate_grid()

        return self._grid

    def get_grid_type(self) -> HexGridType:
        return self._grid_type

    def _generate_grid(self):
        match self._grid_type:
            case HexGridType.XSIGNMAG:
                grid_func = lambda q, r: sm_parity(q) ^ sm_parity(r) ^ sm_parity(-q - r)  # noqa: E731
            case HexGridType.XONESCOMP:
                grid_func = lambda q, r: oc_parity(q) ^ oc_parity(r) ^ oc_parity(-q - r)  # noqa: E731
            case HexGridType.XTWOSCOMP:
                grid_func = lambda q, r: tc_parity(q) ^ tc_parity(r) ^ tc_parity(-q - r)  # noqa: E731
            case HexGridType.XSIGNMAGQR:
                grid_func = lambda q, r: sm_parity(q) ^ sm_parity(r)  # noqa: E731
            case HexGridType.XONESCOMPQR:
                grid_func = lambda q, r: oc_parity(q) ^ oc_parity(r)  # noqa: E731
            case HexGridType.XTWOSCOMPQR:
                grid_func = lambda q, r: tc_parity(q) ^ tc_parity(r)  # noqa: E731
            case _:
                grid_func = lambda q, r: randint(0, 1)  # noqa: E731

        self._grid = {
            (q, r): grid_func(q, r)
            for q in range(-self._grid_dimension + 1, self._grid_dimension)
            for r in range(-self._grid_dimension + 1, self._grid_dimension)
            if -self._grid_dimension < (q + r) < self._grid_dimension
        }

    def get_next_grid(self) -> dict[tuple[int, int], int]:
        self._grid_type_index = (self._grid_type_index + 1) % len(self._grid_types)
        self._grid_type = self._grid_types[self._grid_type_index]
        self._generate_grid()
        return self._grid

    def get_prev_grid(self) -> dict[tuple[int, int], int]:
        self._grid_type_index = (self._grid_type_index - 1) % len(self._grid_types)
        self._grid_type = self._grid_types[self._grid_type_index]
        self._generate_grid()
        return self._grid

    def get_grid_by_name(self, name: str) -> dict[tuple[int, int], int]:
        self._grid_type = HexGridType(name)
        self._generate_grid()
        return self._grid
