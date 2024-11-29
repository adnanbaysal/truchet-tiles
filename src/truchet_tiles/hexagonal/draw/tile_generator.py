from collections import defaultdict

import math
from typing import Any

import drawsvg as dw  # type: ignore

from truchet_tiles.common.enum import Colors, Connector, Filledness
from truchet_tiles.hexagonal.draw.enum import HexTop
from truchet_tiles.hexagonal.hex_grid import (
    Hex,
    HexGeometry,
    Layout,
    ORIENTATIONS,
    Point,
)


class HexTileGenerator(dict):
    def __init__(self, edge_length: int, max_line_width: int = 32) -> None:
        assert edge_length > 0, "edge_length must be positive"

        self._edge_length = edge_length
        self._max_line_width = max_line_width

        self._hex_geometries = self._calc_hex_geometries()

        self._base_tiles: dict[HexTop, dict[Filledness, Any]] = {}
        for key in ORIENTATIONS:
            self._base_tiles[key] = {
                Filledness.linear: {
                    # keys are line_width, values are list of svg elements
                    Connector.straight: defaultdict(list),
                    Connector.curved: defaultdict(list),
                    Connector.twoline: defaultdict(list),
                },
                Filledness.filled: {
                    Connector.straight: [],  # list of svg elements
                    Connector.curved: [],  # list of svg elements
                    Connector.twoline: [],  # list of svg elements
                },
            }

        for line_width in range(1, self._max_line_width + 1):
            self._create_linear_base_tiles(line_width)

        self._create_filled_base_tiles()

    def _calc_hex_geometries(self) -> dict[HexTop, HexGeometry]:
        hex_geometries: dict[HexTop, HexGeometry] = {}

        for hex_top, orientation in ORIENTATIONS.items():
            layout = Layout(
                orientation=orientation,
                size=Point(self._edge_length, self._edge_length),
                origin=Point(0, 0),
            )
            hex_geometry = HexGeometry(layout, Hex(0, 0, 0))
            hex_geometries[hex_top] = hex_geometry

        return hex_geometries

    def __getitem__(self, key: Any) -> Any:
        return self._base_tiles.__getitem__(key)

    # LEVEL 1 base tile functions
    def _create_linear_base_tiles(self, line_width: int):
        self._create_linear_straight_base_tiles(line_width)
        self._create_linear_curved_base_tiles(line_width)
        self._create_linear_twoline_base_tiles(line_width)

    def _create_filled_base_tiles(self):
        self._create_filled_straight_base_tiles()
        self._create_filled_curved_base_tiles()
        self._create_filled_twoline_base_tiles()

    # LEVEL 2 base tile functions
    def _create_linear_straight_base_tiles(self, line_width: int):
        self._create_linear_straight_base_tile(0, line_width)
        self._create_linear_straight_base_tile(1, line_width)

    def _create_linear_curved_base_tiles(self, line_width: int):
        self._create_linear_curved_base_tile(0, line_width)
        self._create_linear_curved_base_tile(1, line_width)

    def _create_linear_twoline_base_tiles(self, line_width: int):
        self._create_linear_twoline_base_tile(0, line_width)
        self._create_linear_twoline_base_tile(1, line_width)

    def _create_filled_straight_base_tiles(self):
        self._create_outside_filled_straight_base_tile(0)
        self._create_outside_filled_straight_base_tile(1)

        self._create_inside_filled_straight_base_tile(0)
        self._create_inside_filled_straight_base_tile(1)

    def _create_filled_curved_base_tiles(self):
        self._create_outside_filled_curved_base_tile(0)
        self._create_outside_filled_curved_base_tile(1)

        self._create_inside_filled_curved_base_tile(0)
        self._create_inside_filled_curved_base_tile(1)

    def _create_filled_twoline_base_tiles(self):
        self._create_outside_filled_twoline_base_tile(0)
        self._create_outside_filled_twoline_base_tile(1)

        self._create_inside_filled_twoline_base_tile(0)
        self._create_inside_filled_twoline_base_tile(1)

    # LEVEL 3 base tile functions
    def _create_linear_straight_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            lines = [
                dw.Line(
                    hex_geometry.edge_mids[2 * i + tile_type].x,
                    hex_geometry.edge_mids[2 * i + tile_type].y,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                    stroke_width=line_width,
                    stroke=Colors.SVG_BLACK,
                )
                for i in range(3)
            ]

            ls = dw.Group(id=f"ls{hex_top.value}{tile_type}", fill="none")
            for i in range(3):
                ls.append(lines[i])

            self._base_tiles[hex_top][Filledness.linear][Connector.straight][
                line_width
            ].append(ls)

    def _create_linear_curved_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            arcs = [
                dw.Path(
                    d=f"""
                        M {hex_geometry.edge_mids[2 * i + tile_type].x} 
                          {hex_geometry.edge_mids[2 * i + tile_type].y}
                        A {self._edge_length / 2} {self._edge_length / 2} 0 0 1 
                          {hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x} 
                          {hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y}
                    """,
                    stroke_width=line_width,
                    stroke=Colors.SVG_BLACK,
                )
                for i in range(3)
            ]

            ls = dw.Group(id=f"lc{hex_top.value}{tile_type}", fill="none")
            for i in range(3):
                ls.append(arcs[i])

            self._base_tiles[hex_top][Filledness.linear][Connector.curved][
                line_width
            ].append(ls)

    def _create_linear_twoline_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            lines = [
                dw.Lines(
                    hex_geometry.edge_mids[2 * i + tile_type].x,
                    hex_geometry.edge_mids[2 * i + tile_type].y,
                    hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].y,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                    stroke_width=line_width,
                    stroke=Colors.SVG_BLACK,
                )
                for i in range(3)
            ]

            ls = dw.Group(id=f"ls{hex_top.value}{tile_type}", fill="none")
            for i in range(3):
                ls.append(lines[i])

            self._base_tiles[hex_top][Filledness.linear][Connector.twoline][
                line_width
            ].append(ls)

    def _create_outside_filled_straight_base_tile(self, tile_type: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            triangles = [
                dw.Lines(
                    hex_geometry.edge_mids[2 * i + tile_type].x,
                    hex_geometry.edge_mids[2 * i + tile_type].y,
                    hex_geometry.corners[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.corners[(2 * i + 1 + tile_type) % 6].y,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                    stroke=Colors.SVG_BLACK,
                    fill=Colors.SVG_BLACK,
                    close=True,
                )
                for i in range(3)
            ]

            fos = dw.Group(id=f"fos{hex_top.value}{tile_type}", fill="none")
            for i in range(3):
                fos.append(triangles[i])

            self._base_tiles[hex_top][Filledness.filled][Connector.straight].append(fos)

    def _create_inside_filled_straight_base_tile(self, tile_type: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            points = []
            for i in range(3):
                points += [
                    hex_geometry.edge_mids[2 * i + tile_type].x,
                    hex_geometry.edge_mids[2 * i + tile_type].y,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                    hex_geometry.corners[(2 * i + 2 + tile_type) % 6].x,
                    hex_geometry.corners[(2 * i + 2 + tile_type) % 6].y,
                ]

            polygon = dw.Lines(
                *points, stroke=Colors.SVG_BLACK, fill=Colors.SVG_BLACK, close=True
            )

            fis = dw.Group(id=f"fis{hex_top.value}{tile_type}", fill="none")
            fis.append(polygon)

            self._base_tiles[hex_top][Filledness.filled][Connector.straight].append(fis)

    def _create_outside_filled_curved_base_tile(self, tile_type: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            arcs = [
                self._create_circle_pie(
                    (
                        hex_geometry.corners[(2 * i + 1 + tile_type) % 6].x,
                        hex_geometry.corners[(2 * i + 1 + tile_type) % 6].y,
                    ),
                )
                for i in range(3)
            ]

            foc = dw.Group(id=f"foc{hex_top.value}{tile_type}", fill="none")
            for i in range(3):
                foc.append(arcs[i])

            self._base_tiles[hex_top][Filledness.filled][Connector.curved].append(foc)

    def _create_inside_filled_curved_base_tile(self, tile_type: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            hexagon_points = []
            for p in hex_geometry.corners:
                hexagon_points += [p.x, p.y]

            black_hexagon = dw.Lines(
                *hexagon_points,
                stroke=Colors.SVG_BLACK,
                fill=Colors.SVG_BLACK,
                closed=True,
            )

            arcs = [
                self._create_circle_pie(
                    (
                        hex_geometry.corners[(2 * i + 1 + tile_type) % 6].x,
                        hex_geometry.corners[(2 * i + 1 + tile_type) % 6].y,
                    ),
                    color=Colors.SVG_WHITE,
                )
                for i in range(3)
            ]

            fic = dw.Group(id=f"fic{hex_top.value}{tile_type}", fill="none")
            fic.append(black_hexagon)
            for i in range(3):
                fic.append(arcs[i])

            self._base_tiles[hex_top][Filledness.filled][Connector.curved].append(fic)

    def _create_circle_pie(self, center: tuple[float, float], color=Colors.SVG_BLACK):
        pie = dw.Circle(
            *center,
            self._edge_length / 2,
            fill=color,
            path_length=math.pi * self._edge_length / 3,
        )
        return pie

    def _create_outside_filled_twoline_base_tile(self, tile_type: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            parallelograms = [
                dw.Lines(
                    hex_geometry.edge_mids[2 * i + tile_type].x,
                    hex_geometry.edge_mids[2 * i + tile_type].y,
                    hex_geometry.corners[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.corners[(2 * i + 1 + tile_type) % 6].y,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                    hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].y,
                    stroke=Colors.SVG_BLACK,
                    fill=Colors.SVG_BLACK,
                    close=True,
                )
                for i in range(3)
            ]

            fos = dw.Group(id=f"fot{hex_top.value}{tile_type}", fill="none")
            for i in range(3):
                fos.append(parallelograms[i])

            self._base_tiles[hex_top][Filledness.filled][Connector.twoline].append(fos)

    def _create_inside_filled_twoline_base_tile(self, tile_type: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            points = []
            for i in range(3):
                points += [
                    hex_geometry.edge_mids[2 * i + tile_type].x,
                    hex_geometry.edge_mids[2 * i + tile_type].y,
                    hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].x,  # ???
                    hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].y,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                    hex_geometry.corners[(2 * i + 2 + tile_type) % 6].x,
                    hex_geometry.corners[(2 * i + 2 + tile_type) % 6].y,
                ]

            polygon = dw.Lines(
                *points, stroke=Colors.SVG_BLACK, fill=Colors.SVG_BLACK, close=True
            )

            fis = dw.Group(id=f"fit{hex_top.value}{tile_type}", fill="none")
            fis.append(polygon)

            self._base_tiles[hex_top][Filledness.filled][Connector.twoline].append(fis)
