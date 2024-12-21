from collections import defaultdict
from enum import Enum
from functools import cache
from random import randint
from typing import Callable

from truchet_tiles.common.math import parity


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
    ZEROS = "zeros"
    ONES = "ones"


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


@cache
def get_hex_grid(
    grid_dimension: int, grid_type: str
) -> defaultdict[tuple[int, int], int]:
    match grid_type:
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
        case HexGridType.ZEROS:
            grid_func = lambda q, r: 0  # noqa: E731
        case HexGridType.ONES:
            grid_func = lambda q, r: 1  # noqa: E731
        case _:
            grid_func = lambda q, r: randint(0, 1)  # noqa: E731

    return defaultdict(
        int,
        (
            ((q, r), grid_func(q, r))
            for q in range(-grid_dimension + 1, grid_dimension)
            for r in range(-grid_dimension + 1, grid_dimension)
            if -grid_dimension < (q + r) < grid_dimension
        ),
    )
