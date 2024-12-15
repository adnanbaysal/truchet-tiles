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
        hex_top: HexTop,
        line_width: int = 1,
        line_color: str = SvgColors.BLACK,
        fill_color: str = SvgColors.BLACK,
        bg_color: str = SvgColors.BLACK,
    ) -> None:
        assert edge_length > 0, "edge_length must be positive"

        self._edge_length = edge_length
        self._line_width = line_width

        self._hex_top = hex_top

        self._line_color = line_color
        self._fill_color = fill_color
        self._bg_color = bg_color

        self._hex_geometry = self._calc_hex_geometry()
        self._hexagon_corners = []
        for p in self._hex_geometry.corners:
            self._hexagon_corners += [p.x, p.y]

        self._base_tiles: dict[Connector, list[dw.Path]] = {
            Connector.line: [],
            Connector.curved: [],
            Connector.twoline: [],
        }

        self._create_base_tiles()

    def _calc_hex_geometry(self) -> HexGeometry:
        orientation = ORIENTATIONS[self._hex_top]
        layout = Layout(
            orientation=orientation,
            size=Point(self._edge_length, self._edge_length),
            origin=Point(0, 0),
        )
        return HexGeometry(layout, Hex(0, 0, 0))

    def _get_bg_hexagon(self, color: str) -> dw.Path:
        return dw.Lines(
            *self._hexagon_corners,
            fill=color,
            closed=True,
        )

    def __getitem__(self, key: Any) -> Any:
        return self._base_tiles.__getitem__(key)

    # LEVEL 1 base tile function
    def _create_base_tiles(self):
        self._create_line_base_tiles()
        self._create_curved_base_tiles()
        self._create_twoline_base_tiles()

    # LEVEL 2 base tile functions
    def _create_line_base_tiles(self):
        self._create_outside_filled_line_base_tile()
        self._create_inside_filled_line_base_tile()

    def _create_curved_base_tiles(self):
        self._create_outside_filled_curved_base_tile()
        self._create_inside_filled_curved_base_tile()

    def _create_twoline_base_tiles(self):
        self._create_outside_filled_twoline_base_tile()
        self._create_inside_filled_twoline_base_tile()

    # LEVEL 3 base tile functions
    def _create_outside_filled_line_base_tile(self):
        lines = self._get_lines(0)
        triangles = [
            dw.Lines(
                self._hex_geometry.edge_mids[2 * i].x,
                self._hex_geometry.edge_mids[2 * i].y,
                self._hex_geometry.corners[(2 * i + 1) % 6].x,
                self._hex_geometry.corners[(2 * i + 1) % 6].y,
                self._hex_geometry.edge_mids[(2 * i + 1) % 6].x,
                self._hex_geometry.edge_mids[(2 * i + 1) % 6].y,
                fill=self._fill_color,
                close=True,
            )
            for i in range(3)
        ]

        ofl = dw.Group(id="ofl", fill="none")
        ofl.append(self._get_bg_hexagon(self._bg_color))
        for i in range(3):
            ofl.append(triangles[i])
        for i in range(3):
            ofl.append(lines[i])

        self._base_tiles[Connector.line].append(ofl)

    def _create_inside_filled_line_base_tile(self):
        lines = self._get_lines(1)
        points = []
        for i in range(3):
            points += [
                self._hex_geometry.edge_mids[2 * i + 1].x,
                self._hex_geometry.edge_mids[2 * i + 1].y,
                self._hex_geometry.edge_mids[(2 * i + 2) % 6].x,
                self._hex_geometry.edge_mids[(2 * i + 2) % 6].y,
                self._hex_geometry.corners[(2 * i + 3) % 6].x,
                self._hex_geometry.corners[(2 * i + 3) % 6].y,
            ]

        polygon = dw.Lines(*points, fill=self._fill_color, close=True)

        ifl = dw.Group(id="ifl", fill="none")
        ifl.append(self._get_bg_hexagon(self._bg_color))
        ifl.append(polygon)
        for i in range(3):
            ifl.append(lines[i])

        self._base_tiles[Connector.line].append(ifl)

    def _create_outside_filled_curved_base_tile(self):
        arcs = self._get_arcs(0)
        pies = [
            self._create_circle_pie(
                start=(
                    self._hex_geometry.edge_mids[(2 * i) % 6].x,
                    self._hex_geometry.edge_mids[(2 * i) % 6].y,
                ),
                center=(
                    self._hex_geometry.corners[(2 * i + 1) % 6].x,
                    self._hex_geometry.corners[(2 * i + 1) % 6].y,
                ),
                end=(
                    self._hex_geometry.edge_mids[(2 * i + 1) % 6].x,
                    self._hex_geometry.edge_mids[(2 * i + 1) % 6].y,
                ),
                fill_color=self._fill_color,
            )
            for i in range(3)
        ]

        ofc = dw.Group(id="ofc", fill="none")
        ofc.append(self._get_bg_hexagon(self._bg_color))
        for i in range(3):
            ofc.append(pies[i])
        for i in range(3):
            ofc.append(arcs[i])

        self._base_tiles[Connector.curved].append(ofc)

    def _create_inside_filled_curved_base_tile(self):
        arcs = self._get_arcs(1)
        pies = [
            self._create_circle_pie(
                start=(
                    self._hex_geometry.edge_mids[(2 * i + 1) % 6].x,
                    self._hex_geometry.edge_mids[(2 * i + 1) % 6].y,
                ),
                center=(
                    self._hex_geometry.corners[(2 * i + 2) % 6].x,
                    self._hex_geometry.corners[(2 * i + 2) % 6].y,
                ),
                end=(
                    self._hex_geometry.edge_mids[(2 * i + 2) % 6].x,
                    self._hex_geometry.edge_mids[(2 * i + 2) % 6].y,
                ),
                fill_color=self._bg_color,
            )
            for i in range(3)
        ]

        ifc = dw.Group(id="ifc", fill="none")
        ifc.append(self._get_bg_hexagon(self._fill_color))
        for i in range(3):
            ifc.append(pies[i])
        for i in range(3):
            ifc.append(arcs[i])

        self._base_tiles[Connector.curved].append(ifc)

    def _create_outside_filled_twoline_base_tile(self):
        twolines = self._get_twolines(0)
        parallelograms = [
            dw.Lines(
                self._hex_geometry.edge_mids[2 * i].x,
                self._hex_geometry.edge_mids[2 * i].y,
                self._hex_geometry.corners[(2 * i + 1) % 6].x,
                self._hex_geometry.corners[(2 * i + 1) % 6].y,
                self._hex_geometry.edge_mids[(2 * i + 1) % 6].x,
                self._hex_geometry.edge_mids[(2 * i + 1) % 6].y,
                self._hex_geometry.half_hex_corners[(2 * i + 1) % 6].x,
                self._hex_geometry.half_hex_corners[(2 * i + 1) % 6].y,
                fill=self._fill_color,
                close=True,
            )
            for i in range(3)
        ]

        oft = dw.Group(id="oft", fill="none")
        oft.append(self._get_bg_hexagon(self._bg_color))
        for i in range(3):
            oft.append(parallelograms[i])
        for i in range(3):
            oft.append(twolines[i])

        self._base_tiles[Connector.twoline].append(oft)

    def _create_inside_filled_twoline_base_tile(self):
        twolines = self._get_twolines(1)
        points = []
        for i in range(3):
            points += [
                self._hex_geometry.edge_mids[2 * i + 1].x,
                self._hex_geometry.edge_mids[2 * i + 1].y,
                self._hex_geometry.half_hex_corners[(2 * i + 2) % 6].x,
                self._hex_geometry.half_hex_corners[(2 * i + 2) % 6].y,
                self._hex_geometry.edge_mids[(2 * i + 2) % 6].x,
                self._hex_geometry.edge_mids[(2 * i + 2) % 6].y,
                self._hex_geometry.corners[(2 * i + 3) % 6].x,
                self._hex_geometry.corners[(2 * i + 3) % 6].y,
            ]

        polygon = dw.Lines(*points, fill=self._fill_color, close=True)

        ift = dw.Group(id="fit", fill="none")
        ift.append(self._get_bg_hexagon(self._bg_color))
        ift.append(polygon)
        for i in range(3):
            ift.append(twolines[i])

        self._base_tiles[Connector.twoline].append(ift)

    # Helper functions
    def _get_lines(self, tile_type: int) -> list[dw.Line]:
        return [
            dw.Line(
                self._hex_geometry.edge_mids[2 * i + tile_type].x,
                self._hex_geometry.edge_mids[2 * i + tile_type].y,
                self._hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                self._hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                stroke_width=self._line_width,
                stroke=self._line_color,
            )
            for i in range(3)
        ]

    def _get_arcs(self, tile_type: int) -> list[dw.Path]:
        return [
            dw.Path(
                d=(
                    f"M {self._hex_geometry.edge_mids[2 * i + tile_type].x} "
                    f"{self._hex_geometry.edge_mids[2 * i + tile_type].y} "
                    f"A {self._edge_length / 2} {self._edge_length / 2} 0 0 1 "
                    f"{self._hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x} "
                    f"{self._hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y}"
                ),
                stroke_width=self._line_width,
                stroke=self._line_color,
            )
            for i in range(3)
        ]

    def _get_twolines(self, tile_type: int) -> list[dw.Lines]:
        return [
            dw.Lines(
                self._hex_geometry.edge_mids[2 * i + tile_type].x,
                self._hex_geometry.edge_mids[2 * i + tile_type].y,
                self._hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].x,
                self._hex_geometry.half_hex_corners[(2 * i + 1 + tile_type) % 6].y,
                self._hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
                self._hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
                stroke_width=self._line_width,
                stroke=self._line_color,
            )
            for i in range(3)
        ]

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
