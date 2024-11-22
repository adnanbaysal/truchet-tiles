from collections import defaultdict

# import math
from typing import Any

import drawsvg as dw  # type: ignore

from truchet_tiles.hexagonal.draw.enum import Colors, Curvedness, Filledness, HexTop
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
                    Curvedness.straight: defaultdict(list),
                    Curvedness.curved: defaultdict(list),
                },
                Filledness.filled: {
                    Curvedness.straight: [],  # list of svg elements
                    Curvedness.curved: [],  # list of svg elements
                },
            }

        for line_width in range(1, self._max_line_width + 1):
            self._create_linear_base_tiles(line_width)

        # self._create_filled_base_tiles()

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

    # def _create_filled_base_tiles(self):
    #     self._create_filled_straight_base_tiles()
    #     self._create_filled_curved_base_tiles()

    # LEVEL 2 base tile functions
    def _create_linear_straight_base_tiles(self, line_width: int):
        self._create_linear_straight_base_tile(0, line_width)
        self._create_linear_straight_base_tile(1, line_width)

    def _create_linear_curved_base_tiles(self, line_width: int):
        self._create_linear_curved_base_tile(0, line_width)
        self._create_linear_curved_base_tile(1, line_width)

    # def _create_filled_straight_base_tiles(self):
    #     # Fill area out of diagonal lines
    #     self._create_outside_filled_straight_base_tile(0)
    #     self._create_outside_filled_straight_base_tile(1)

    #     # Fill area beween diagonal lines
    #     self._create_inside_filled_straight_base_tile(0)
    #     self._create_inside_filled_straight_base_tile(1)

    # def _create_filled_curved_base_tiles(self):
    #     # Fill area outside of arc lines
    #     self._create_outside_filled_curved_base_tile(0)
    #     self._create_outside_filled_curved_base_tile(1)

    #     # Fill area between arc lines
    #     self._create_inside_filled_curved_base_tile(0)
    #     self._create_inside_filled_curved_base_tile(1)

    # LEVEL 3 base tile functions
    def _create_linear_straight_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            lines = [
                dw.Line(
                    hex_geometry.mids[2 * i + tile_type].x,
                    hex_geometry.mids[2 * i + tile_type].y,
                    hex_geometry.mids[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.mids[(2 * i + 1 + tile_type) % 6].y,
                    stroke_width=line_width,
                    stroke=Colors.SVG_BLACK,
                )
                for i in range(3)
            ]

            ls = dw.Group(id=f"ls{hex_top.value}{tile_type}", fill="none")
            for i in range(3):
                ls.append(lines[i])

            self._base_tiles[hex_top][Filledness.linear][Curvedness.straight][
                line_width
            ].append(ls)

    def _create_linear_curved_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            arcs = [
                dw.Path(
                    d=f"""
                        M {hex_geometry.mids[2 * i + tile_type].x} {hex_geometry.mids[2 * i + tile_type].y}
                        A {self._edge_length / 2} {self._edge_length / 2} 0 0 1 
                          {hex_geometry.mids[(2 * i + 1 + tile_type) % 6].x} 
                          {hex_geometry.mids[(2 * i + 1 + tile_type) % 6].y}
                    """,
                    stroke_width=line_width,
                    stroke=Colors.SVG_BLACK,
                )
                for i in range(3)
            ]

            ls = dw.Group(id=f"lc{hex_top.value}{tile_type}", fill="none")
            for i in range(3):
                ls.append(arcs[i])

            self._base_tiles[hex_top][Filledness.linear][Curvedness.curved][
                line_width
            ].append(ls)

    # def _create_outside_filled_straight_base_tile(self, tile_type: int):
    #     left0 = (0, self._mid)
    #     right0 = (self._r_outer, self._mid)

    #     if tile_type == 0:
    #         left1 = (self._mid, self._r_outer)
    #         left2 = (0, self._r_outer)
    #         right1 = (self._mid, 0)
    #         right2 = (self._r_outer, 0)
    #     else:
    #         left1 = (self._mid, 0)
    #         left2 = (0, 0)
    #         right1 = (self._mid, self._r_outer)
    #         right2 = (self._r_outer, self._r_outer)

    #     triangle_left = dw.Lines(
    #         *left0,
    #         *left1,
    #         *left2,
    #         fill=Colors.SVG_BLACK,
    #         stroke=Colors.SVG_BLACK,
    #         close="true",
    #     )

    #     triangle_right = dw.Lines(
    #         *right0,
    #         *right1,
    #         *right2,
    #         fill=Colors.SVG_BLACK,
    #         stroke=Colors.SVG_BLACK,
    #         close="true",
    #     )

    #     fos = dw.Group(id=f"fos{tile_type}", fill="none")
    #     fos.append(triangle_left)
    #     fos.append(triangle_right)

    #     self._base_tiles[Filledness.filled][Curvedness.straight].append(fos)

    # def _get_hexagon_points(self, tile_type: int):
    #     p0 = (0, self._mid)
    #     p3 = (self._r_outer, self._mid)

    #     if tile_type == 0:
    #         p1 = (self._mid, self._r_outer)
    #         p2 = (self._r_outer, self._r_outer)
    #         p4 = (self._mid, 0)
    #         p5 = (0, 0)
    #     else:
    #         p1 = (0, self._r_outer)
    #         p2 = (self._mid, self._r_outer)
    #         p4 = (self._r_outer, 0)
    #         p5 = (self._mid, 0)

    #     return (*p0, *p1, *p2, *p3, *p4, *p5)

    # def _create_inside_filled_straight_base_tile(self, tile_type: int):
    #     hexagon_points = self._get_hexagon_points(tile_type)

    #     hexagon = dw.Lines(
    #         *hexagon_points,
    #         fill=Colors.SVG_BLACK,
    #         stroke=Colors.SVG_BLACK,
    #         close="true",
    #     )

    #     fis = dw.Group(id=f"fis{tile_type}", fill="none")
    #     fis.append(hexagon)

    #     self._base_tiles[Filledness.filled][Curvedness.straight].append(fis)

    # def _create_outside_filled_curved_base_tile(self, tile_type: int):
    #     if tile_type == 1:
    #         left_center = (0, 0)
    #         right_center = (self._r_outer, self._r_outer)
    #     else:
    #         left_center = (0, self._r_outer)
    #         right_center = (self._r_outer, 0)

    #     pie_left = self._create_circle_pie(left_center)
    #     pie_right = self._create_circle_pie(right_center)

    #     foc = dw.Group(id=f"foc{tile_type}", fill="none")
    #     foc.append(pie_left)
    #     foc.append(pie_right)

    #     self._base_tiles[Filledness.filled][Curvedness.curved].append(foc)

    # def _create_inside_filled_curved_base_tile(self, tile_type: int):
    #     if tile_type == 1:
    #         la_center = (0, 0)
    #         ra_center = (self._r_outer, self._r_outer)
    #     else:
    #         la_center = (0, self._r_outer)
    #         ra_center = (self._r_outer, 0)

    #     pie_left = self._create_circle_pie(la_center, color=Colors.SVG_WHITE)
    #     pie_right = self._create_circle_pie(ra_center, color=Colors.SVG_WHITE)

    #     hexagon_points = self._get_hexagon_points(tile_type)
    #     black_hexagon = dw.Lines(
    #         *hexagon_points,
    #         stroke=Colors.SVG_BLACK,
    #         fill=Colors.SVG_BLACK,
    #         closed=True,
    #     )

    #     fic = dw.Group(id=f"fic{tile_type}", fill="none")
    #     fic.append(black_hexagon)
    #     fic.append(pie_left)
    #     fic.append(pie_right)

    #     self._base_tiles[Filledness.filled][Curvedness.curved].append(fic)

    # def _create_circle_pie(self, center, color=Colors.SVG_BLACK):
    #     pie = dw.Circle(
    #         *center,
    #         self._mid,
    #         fill=color,
    #         path_length=math.pi * self._mid / 2,
    #     )
    #     return pie
