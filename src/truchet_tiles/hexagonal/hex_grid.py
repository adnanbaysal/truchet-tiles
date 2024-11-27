# NOTE: Adapted from: https://www.redblobgames.com/grids/hexagons/

from dataclasses import dataclass
import math

from truchet_tiles.hexagonal.draw.enum import HexTop


@dataclass
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Hex:
    q: int
    r: int
    s: int

    def __post_init__(self):
        if self.q + self.r + self.s != 0:
            raise ValueError("q + r + s should be 0")

    def __abs__(self) -> int:
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2


@dataclass
class Orientation:
    f0: float
    f1: float
    f2: float
    f3: float
    start_angle: float


ORIENTATIONS: dict[HexTop, Orientation] = {
    HexTop.flat: Orientation(
        math.sqrt(3.0),
        math.sqrt(3.0) / 2.0,
        0.0,
        3.0 / 2.0,
        0.5,
    ),
    HexTop.pointy: Orientation(
        3.0 / 2.0,
        0.0,
        math.sqrt(3.0) / 2.0,
        math.sqrt(3.0),
        0.0,
    ),
}


@dataclass
class Layout:
    orientation: Orientation
    size: Point
    origin: Point


class HexGeometry:
    def __init__(self, layout: Layout, hex_: Hex) -> None:
        self._layout = layout
        self._hex = hex_

        self.center = self._calc_center()
        self.corners = self._calc_corners()
        self.edge_mids = self._calc_edge_mids()
        self.half_hex_corners = self._calc_half_hex_corners()

    def _calc_center(self) -> Point:
        M = self._layout.orientation
        size = self._layout.size
        origin = self._layout.origin
        x = (M.f0 * self._hex.q + M.f1 * self._hex.r) * size.x
        y = (M.f2 * self._hex.q + M.f3 * self._hex.r) * size.y
        return Point(x + origin.x, y + origin.y)

    def _hex_corner_offset(self, corner: int) -> Point:
        M = self._layout.orientation
        size = self._layout.size
        angle = 2.0 * math.pi * (M.start_angle - corner) / 6.0
        return Point(size.x * math.cos(angle), size.y * math.sin(angle))

    def _calc_corners(self) -> tuple[Point, Point, Point, Point, Point, Point]:
        corners = []
        for i in range(6):
            offset = self._hex_corner_offset(i)
            corners.append(Point(self.center.x + offset.x, self.center.y + offset.y))

        return tuple(corners)  # type: ignore

    def _calc_edge_mids(self) -> tuple[Point, Point, Point, Point, Point, Point]:
        mids = []
        for i in range(6):
            p1 = self.corners[i]
            p2 = self.corners[(i + 1) % 6]
            mid_point = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
            mids.append(mid_point)

        return tuple(mids)  # type: ignore

    def _calc_half_hex_corners(self) -> tuple[Point, Point, Point, Point, Point, Point]:
        half_hex_corners = []
        for i in range(6):
            p = self.corners[i]
            mid_point = Point((p.x + self.center.x) / 2, (p.y + self.center.y) / 2)
            half_hex_corners.append(mid_point)

        return tuple(half_hex_corners)  # type: ignore


@dataclass
class HexGridData:
    value: int
    center: Point
    corners: tuple[Point, Point, Point, Point, Point, Point]
    mids: tuple[Point, Point, Point, Point, Point, Point]

    def __post_init__(self):
        if self.value not in (0, 1):
            raise ValueError("value should be 0 or 1")


class HexGrid(dict):
    def __init__(
        self,
        hex_grid: dict[tuple[int, int], int],
        layout: Layout,
    ) -> None:
        self._hex_grid: dict[Hex, HexGridData] = {}
        self._layout = layout
        self._calculate_hex_grid(hex_grid)

    def __getitem__(self, key: Hex) -> HexGridData:
        return self._hex_grid.__getitem__(key)

    def keys(self):
        return self._hex_grid.keys()

    def values(self):
        return self._hex_grid.values()

    def items(self):
        return self._hex_grid.items()

    def _calculate_hex_grid(self, hex_grid: dict[tuple[int, int], int]):
        for key, value in hex_grid.items():
            q, r = key
            s = -q - r
            hex_ = Hex(q, r, s)

            hex_geometry = HexGeometry(self._layout, hex_)
            center = hex_geometry.center
            corners = hex_geometry.corners
            mids = hex_geometry.edge_mids

            self._hex_grid[Hex(q, r, s)] = HexGridData(
                value=value,
                center=center,
                corners=corners,
                mids=mids,
            )
