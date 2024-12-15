from collections import defaultdict

from typing import Any

import drawsvg as dw  # type: ignore

from truchet_tiles.common.enum import SvgColors, Connector
from truchet_tiles.hexagonal.draw.enum import HexTop
from truchet_tiles.hexagonal.hex_grid import (
    Hex,
    HexGeometry,
    Layout,
    ORIENTATIONS,
    Point,
)


class HexTileGenerator(dict):
    def __init__(
        self,
        edge_length: int,
        max_line_width: int = 32,
        line_color: str = SvgColors.BLACK,
        fill_color: str = SvgColors.BLACK,
        bg_color: str = SvgColors.BLACK,
    ) -> None:
        assert edge_length > 0, "edge_length must be positive"

        self._edge_length = edge_length
        self._max_line_width = max_line_width

        self._line_color = line_color
        self._fill_color = fill_color
        self._bg_color = bg_color

        self._hex_geometries = self._calc_hex_geometries()
        self._bg_hexagons = self._get_bg_hexagons()

        self._base_tiles: dict[
            HexTop, dict[Filledness, dict[Connector, defaultdict[int, list[dw.Path]]]]
        ] = {}
        for key in ORIENTATIONS:
            self._base_tiles[key] = {
                Filledness.linear: {
                    # keys are line_width, values are list of svg elements
                    Connector.line: defaultdict(list),
                    Connector.curved: defaultdict(list),
                    Connector.twoline: defaultdict(list),
                },
                Filledness.filled: {
                    # keys are line_width, values are list of svg elements
                    Connector.line: defaultdict(list),
                    Connector.curved: defaultdict(list),
                    Connector.twoline: defaultdict(list),
                },
            }

        for line_width in range(1, self._max_line_width + 1):
            self._create_linear_base_tiles(line_width)
            self._create_filled_base_tiles(line_width)

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

    def _get_bg_hexagons(self) -> dict[HexTop, dict[str, dw.Path]]:
        bg_hexagons: dict[HexTop, dict[str, dw.Path]] = {
            HexTop.flat: {},
            HexTop.pointy: {},
        }

        for hex_top, hex_geometry in self._hex_geometries.items():
            for color in (self._fill_color, self._bg_color):
                hexagon_points = []
                for p in hex_geometry.corners:
                    hexagon_points += [p.x, p.y]

                bg_hexagons[hex_top][color] = dw.Lines(
                    *hexagon_points,
                    fill=color,
                    closed=True,
                )

        return bg_hexagons

    def __getitem__(self, key: Any) -> Any:
        return self._base_tiles.__getitem__(key)

    # LEVEL 1 base tile functions
    def _create_linear_base_tiles(self, line_width: int):
        self._create_linear_straight_base_tiles(line_width)
        self._create_linear_curved_base_tiles(line_width)
        self._create_linear_twoline_base_tiles(line_width)

    def _create_filled_base_tiles(self, line_width: int):
        self._create_filled_straight_base_tiles(line_width)
        self._create_filled_curved_base_tiles(line_width)
        self._create_filled_twoline_base_tiles(line_width)

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

    def _create_filled_straight_base_tiles(self, line_width: int):
        self._create_outside_filled_straight_base_tile(0, line_width)
        self._create_inside_filled_straight_base_tile(1, line_width)

    def _create_filled_curved_base_tiles(self, line_width: int):
        self._create_outside_filled_curved_base_tile(0, line_width)
        self._create_inside_filled_curved_base_tile(1, line_width)

    def _create_filled_twoline_base_tiles(self, line_width: int):
        self._create_outside_filled_twoline_base_tile(0, line_width)
        self._create_inside_filled_twoline_base_tile(1, line_width)

    # LEVEL 3 base tile functions
    def _get_lines(
        self,
        tile_type: int,
        line_width: int,
        hex_geometry: HexGeometry,
    ) -> list[dw.Line]:
        return [
            dw.Line(
                hex_geometry.edge_mids[2 * i + tile_type].x,
                hex_geometry.edge_mids[2 * i + tile_type].y,
                hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                stroke_width=line_width,
                stroke=self._line_color,
            )
            for i in range(3)
        ]

    def _create_linear_straight_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            lines = self._get_lines(tile_type, line_width, hex_geometry)

            ls = dw.Group(id=f"ls{hex_top.value}{tile_type}", fill="none")
            ls.append(self._bg_hexagons[hex_top][self._bg_color])
            for i in range(3):
                ls.append(lines[i])

            self._base_tiles[hex_top][Filledness.linear][Connector.line][
                line_width
            ].append(ls)

    def _get_arcs(
        self,
        tile_type: int,
        line_width: int,
        hex_geometry: HexGeometry,
    ) -> list[dw.Path]:
        return [
            dw.Path(
                d=(
                    f"M {hex_geometry.edge_mids[2 * i + tile_type].x} "
                    f"{hex_geometry.edge_mids[2 * i + tile_type].y} "
                    f"A {self._edge_length / 2} {self._edge_length / 2} 0 0 1 "
                    f"{hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x} "
                    f"{hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y}"
                ),
                stroke_width=line_width,
                stroke=self._line_color,
            )
            for i in range(3)
        ]

    def _create_linear_curved_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            arcs = self._get_arcs(tile_type, line_width, hex_geometry)

            lc = dw.Group(id=f"lc{hex_top.value}{tile_type}", fill="none")
            lc.append(self._bg_hexagons[hex_top][self._bg_color])
            for i in range(3):
                lc.append(arcs[i])

            self._base_tiles[hex_top][Filledness.linear][Connector.curved][
                line_width
            ].append(lc)

    def _get_twolines(
        self,
        tile_type: int,
        line_width: int,
        hex_geometry: HexGeometry,
    ) -> list[dw.Lines]:
        return [
            dw.Lines(
                hex_geometry.edge_mids[2 * i + tile_type].x,
                hex_geometry.edge_mids[2 * i + tile_type].y,
                hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].x,
                hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].y,
                hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                stroke_width=line_width,
                stroke=self._line_color,
            )
            for i in range(3)
        ]

    def _create_linear_twoline_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            two_lines = self._get_twolines(tile_type, line_width, hex_geometry)

            lt = dw.Group(id=f"lt{hex_top.value}{tile_type}", fill="none")
            lt.append(self._bg_hexagons[hex_top][self._bg_color])
            for i in range(3):
                lt.append(two_lines[i])

            self._base_tiles[hex_top][Filledness.linear][Connector.twoline][
                line_width
            ].append(lt)

    def _create_outside_filled_straight_base_tile(
        self, tile_type: int, line_width: int
    ):
        for hex_top, hex_geometry in self._hex_geometries.items():
            lines = self._get_lines(tile_type, line_width, hex_geometry)
            triangles = [
                dw.Lines(
                    hex_geometry.edge_mids[2 * i + tile_type].x,
                    hex_geometry.edge_mids[2 * i + tile_type].y,
                    hex_geometry.corners[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.corners[(2 * i + 1 + tile_type) % 6].y,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                    fill=self._fill_color,
                    close=True,
                )
                for i in range(3)
            ]

            fos = dw.Group(id=f"fos{hex_top.value}{tile_type}", fill="none")
            fos.append(self._bg_hexagons[hex_top][self._bg_color])
            for i in range(3):
                fos.append(triangles[i])
            for i in range(3):
                fos.append(lines[i])

            self._base_tiles[hex_top][Filledness.filled][Connector.line][
                line_width
            ].append(fos)

    def _create_inside_filled_straight_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            lines = self._get_lines(tile_type, line_width, hex_geometry)
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

            polygon = dw.Lines(*points, fill=self._fill_color, close=True)

            fis = dw.Group(id=f"fis{hex_top.value}{tile_type}", fill="none")
            fis.append(
                self._bg_hexagons[hex_top][self._bg_color]
            )  # since the polygon is already filled
            fis.append(polygon)
            for i in range(3):
                fis.append(lines[i])

            self._base_tiles[hex_top][Filledness.filled][Connector.line][
                line_width
            ].append(fis)

    def _create_circle_pie(
        self,
        start: tuple[float, float],
        center: tuple[float, float],
        end: tuple[float, float],
        fill_color: str,
    ) -> dw.Path:
        r = self._edge_length / 2
        pie = dw.Path(
            d=(
                f"M {start[0]} {start[1]}"
                f"A {r} {r} 0 0 1 {end[0]} {end[1]}"
                f"L {center[0]} {center[1]}"
                "Z"
            ),
            fill=fill_color,
        )
        return pie

    def _create_outside_filled_curved_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            arcs = self._get_arcs(tile_type, line_width, hex_geometry)
            pies = [
                self._create_circle_pie(
                    start=(
                        hex_geometry.edge_mids[(2 * i + tile_type) % 6].x,
                        hex_geometry.edge_mids[(2 * i + tile_type) % 6].y,
                    ),
                    center=(
                        hex_geometry.corners[(2 * i + 1 + tile_type) % 6].x,
                        hex_geometry.corners[(2 * i + 1 + tile_type) % 6].y,
                    ),
                    end=(
                        hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                        hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                    ),
                    fill_color=self._fill_color,
                )
                for i in range(3)
            ]

            foc = dw.Group(id=f"foc{hex_top.value}{tile_type}", fill="none")
            foc.append(self._bg_hexagons[hex_top][self._bg_color])
            for i in range(3):
                foc.append(pies[i])
            for i in range(3):
                foc.append(arcs[i])

            self._base_tiles[hex_top][Filledness.filled][Connector.curved][
                line_width
            ].append(foc)

    def _create_inside_filled_curved_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            arcs = self._get_arcs(tile_type, line_width, hex_geometry)
            pies = [
                self._create_circle_pie(
                    start=(
                        hex_geometry.edge_mids[(2 * i + tile_type) % 6].x,
                        hex_geometry.edge_mids[(2 * i + tile_type) % 6].y,
                    ),
                    center=(
                        hex_geometry.corners[(2 * i + 1 + tile_type) % 6].x,
                        hex_geometry.corners[(2 * i + 1 + tile_type) % 6].y,
                    ),
                    end=(
                        hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                        hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                    ),
                    fill_color=self._bg_color,
                )
                for i in range(3)
            ]

            fic = dw.Group(id=f"fic{hex_top.value}{tile_type}", fill="none")
            fic.append(self._bg_hexagons[hex_top][self._fill_color])
            for i in range(3):
                fic.append(pies[i])
            for i in range(3):
                fic.append(arcs[i])

            self._base_tiles[hex_top][Filledness.filled][Connector.curved][
                line_width
            ].append(fic)

    def _create_outside_filled_twoline_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            twolines = self._get_twolines(tile_type, line_width, hex_geometry)
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
                    fill=self._fill_color,
                    close=True,
                )
                for i in range(3)
            ]

            fot = dw.Group(id=f"fot{hex_top.value}{tile_type}", fill="none")
            fot.append(self._bg_hexagons[hex_top][self._bg_color])
            for i in range(3):
                fot.append(parallelograms[i])
            for i in range(3):
                fot.append(twolines[i])

            self._base_tiles[hex_top][Filledness.filled][Connector.twoline][
                line_width
            ].append(fot)

    def _create_inside_filled_twoline_base_tile(self, tile_type: int, line_width: int):
        for hex_top, hex_geometry in self._hex_geometries.items():
            twolines = self._get_twolines(tile_type, line_width, hex_geometry)
            points = []
            for i in range(3):
                points += [
                    hex_geometry.edge_mids[2 * i + tile_type].x,
                    hex_geometry.edge_mids[2 * i + tile_type].y,
                    hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].y,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                    hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                    hex_geometry.corners[(2 * i + 2 + tile_type) % 6].x,
                    hex_geometry.corners[(2 * i + 2 + tile_type) % 6].y,
                ]

            polygon = dw.Lines(*points, fill=self._fill_color, close=True)

            fit = dw.Group(id=f"fit{hex_top.value}{tile_type}", fill="none")
            fit.append(
                self._bg_hexagons[hex_top][self._bg_color]
            )  # since polygon is already filled
            fit.append(polygon)
            for i in range(3):
                fit.append(twolines[i])

            self._base_tiles[hex_top][Filledness.filled][Connector.twoline][
                line_width
            ].append(fit)
