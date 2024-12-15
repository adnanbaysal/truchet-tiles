import math
from typing import Any

import drawsvg as dw  # type: ignore

from truchet_tiles.common.enum import SvgColors, Connector


class RectTileGenerator(dict):
    def __init__(
        self,
        edge_length: int,
        line_width: int = 1,
        line_color: str = SvgColors.BLACK,
        fill_color: str = SvgColors.WHITE,
        bg_color: str = SvgColors.WHITE,
    ) -> None:
        assert edge_length > 0, "tile_size must be positive"
        self._end = edge_length
        self._mid = int(self._end / 2)
        self._line_width = line_width

        self._line_color = line_color
        self._fill_color = fill_color
        self._bg_color = bg_color

        # self._bg_squares = self._get_bg_squares()
        self._square_points = [0, 0, self._end, 0, self._end, self._end, 0, self._end]

        self._base_tiles: dict[Connector, list[dw.Path]] = {
            Connector.line: [],
            Connector.curved: [],
            Connector.twoline: [],
        }

        self._create_base_tiles()

    def __getitem__(self, key: Any) -> Any:
        return self._base_tiles.__getitem__(key)

    def _get_bg_square(self, color: str) -> dw.Lines:
        return dw.Lines(
            *self._square_points,
            fill=color,
            close=True,
        )

    # LEVEL 1 base tile function
    def _create_base_tiles(self):
        self._create_line_base_tiles()
        self._create_filled_curved_base_tiles()
        self._create_filled_twoline_base_tiles()

    # LEVEL 2 base tile functions
    def _create_line_base_tiles(self):
        # Fill area out of diagonal lines
        self._create_outside_filled_line_base_tile(0)
        self._create_outside_filled_line_base_tile(1)

        # Fill area beween diagonal lines
        self._create_inside_filled_line_base_tile(0)
        self._create_inside_filled_line_base_tile(1)

    def _create_filled_curved_base_tiles(self):
        # Fill area outside of arc lines
        self._create_outside_filled_curved_base_tile(0)
        self._create_outside_filled_curved_base_tile(1)

        # Fill area between arc lines
        self._create_inside_filled_curved_base_tile(0)
        self._create_inside_filled_curved_base_tile(1)

    def _create_filled_twoline_base_tiles(self):
        # Fill area outside of arc lines
        self._create_outside_filled_twoline_base_tile(0)
        self._create_outside_filled_twoline_base_tile(1)

        # Fill area between arc lines
        self._create_inside_filled_twoline_base_tile(0)
        self._create_inside_filled_twoline_base_tile(1)

    # LEVEL 3 base tile functions
    def _create_outside_filled_line_base_tile(self, tile_type: int):
        ofl = dw.Group(id=f"ofl{tile_type}", fill="none")
        ofl.append(self._get_bg_square(self._bg_color))

        left0, left1, left2, right0, right1, right2 = self._get_line_points(tile_type)
        triangle_left = dw.Lines(
            *left0,
            *left1,
            *left2,
            fill=self._fill_color,
            close=True,
        )
        triangle_right = dw.Lines(
            *right0,
            *right1,
            *right2,
            fill=self._fill_color,
            close=True,
        )
        ofl.append(triangle_left)
        ofl.append(triangle_right)

        line_left, line_right = self._get_lines(tile_type)
        ofl.append(line_left)
        ofl.append(line_right)

        self._base_tiles[Connector.line].append(ofl)

    def _create_inside_filled_line_base_tile(self, tile_type: int):
        ifl = dw.Group(id=f"ifl{tile_type}", fill="none")
        ifl.append(self._get_bg_square(self._bg_color))

        hexagon_points = self._get_hexagon_points(tile_type)
        hexagon = dw.Lines(
            *hexagon_points,
            fill=self._fill_color,
            close=True,
        )
        ifl.append(hexagon)

        line_left, line_right = self._get_lines(tile_type)
        ifl.append(line_left)
        ifl.append(line_right)

        self._base_tiles[Connector.line].append(ifl)

    def _create_outside_filled_curved_base_tile(self, tile_type: int):
        ofc = dw.Group(id=f"ofc{tile_type}", fill="none")
        ofc.append(self._get_bg_square(self._bg_color))

        left_start, left_center, left_end, right_start, right_center, right_end = (
            self._get_arc_points(tile_type)
        )
        pie_left = self._create_circle_pie(
            left_start, left_center, left_end, self._fill_color
        )
        pie_right = self._create_circle_pie(
            right_start, right_center, right_end, self._fill_color
        )
        ofc.append(pie_left)
        ofc.append(pie_right)

        curve_left, curve_right = self._get_arcs(tile_type)
        ofc.append(curve_left)
        ofc.append(curve_right)

        self._base_tiles[Connector.curved].append(ofc)

    def _create_inside_filled_curved_base_tile(self, tile_type: int):
        ifc = dw.Group(id=f"ifc{tile_type}", fill="none")
        ifc.append(self._get_bg_square(self._fill_color))

        left_start, left_center, left_end, right_start, right_center, right_end = (
            self._get_arc_points(tile_type)
        )
        pie_left = self._create_circle_pie(
            left_start, left_center, left_end, self._bg_color
        )
        pie_right = self._create_circle_pie(
            right_start, right_center, right_end, self._bg_color
        )
        ifc.append(pie_left)
        ifc.append(pie_right)

        curve_left, curve_right = self._get_arcs(tile_type)
        ifc.append(curve_left)
        ifc.append(curve_right)

        self._base_tiles[Connector.curved].append(ifc)

    def _create_outside_filled_twoline_base_tile(self, tile_type: int):
        oft = dw.Group(id=f"oft{tile_type}", fill="none")
        oft.append(self._get_bg_square(self._bg_color))

        left0, left1, left2, left3, right0, right1, right2, right3 = (
            self._get_twoline_points(tile_type)
        )
        poly_left = dw.Lines(
            *left0,
            *left1,
            *left2,
            *left3,
            fill=self._fill_color,
            close=True,
        )
        poly_right = dw.Lines(
            *right0,
            *right1,
            *right2,
            *right3,
            fill=self._fill_color,
            close=True,
        )
        oft.append(poly_left)
        oft.append(poly_right)

        lines_left, lines_right = self._get_twolines(tile_type)
        oft.append(lines_left)
        oft.append(lines_right)

        self._base_tiles[Connector.twoline].append(oft)

    def _create_inside_filled_twoline_base_tile(self, tile_type: int):
        ift = dw.Group(id=f"ift{tile_type}", fill="none")
        ift.append(self._get_bg_square(self._bg_color))

        octagon_points = self._get_octagon_points(tile_type)
        octagon = dw.Lines(
            *octagon_points,
            fill=self._fill_color,
            close=True,
        )
        ift.append(octagon)

        lines_left, lines_right = self._get_twolines(tile_type)
        ift.append(lines_left)
        ift.append(lines_right)

        self._base_tiles[Connector.twoline].append(ift)

    # Helper functions
    def _get_line_points(self, tile_type: int):
        left0 = (0, self._mid)
        right0 = (self._end, self._mid)

        if tile_type == 0:
            left1 = (self._mid, self._end)
            left2 = (0, self._end)
            right1 = (self._mid, 0)
            right2 = (self._end, 0)
        else:
            left1 = (self._mid, 0)
            left2 = (0, 0)
            right1 = (self._mid, self._end)
            right2 = (self._end, self._end)

        return left0, left1, left2, right0, right1, right2

    def _get_lines(self, tile_type: int) -> tuple[dw.Line, dw.Line]:
        left0, left1, _, right0, right1, _ = self._get_line_points(tile_type)

        line_left = dw.Line(
            *left0, *left1, stroke_width=self._line_width, stroke=self._line_color
        )
        line_right = dw.Line(
            *right0, *right1, stroke_width=self._line_width, stroke=self._line_color
        )
        return line_left, line_right

    def _get_arcs(self, tile_type: int) -> tuple[dw.Arc, dw.Arc]:
        if tile_type == 1:
            left_center = (0, 0)
            left_degrees = (90, 0)
            right_center = (self._end, self._end)
            right_degrees = (270, 180)
        else:
            left_center = (0, self._end)
            left_degrees = (360, 270)
            right_center = (self._end, 0)
            right_degrees = (180, 90)

        curve_left = dw.Arc(
            *left_center,
            self._mid,
            *left_degrees,
            stroke_width=self._line_width,
            stroke=self._line_color,
        )
        curve_right = dw.Arc(
            *right_center,
            self._mid,
            *right_degrees,
            stroke_width=self._line_width,
            stroke=self._line_color,
        )

        return curve_left, curve_right

    def _get_twoline_points(self, tile_type: int):
        left0 = (0, self._mid)
        right0 = (self._end, self._mid)
        arcMid = self._end * math.sqrt(2) / 4

        if tile_type == 0:
            left1 = (arcMid, self._end - arcMid)
            left2 = (self._mid, self._end)
            left3 = (0, self._end)
            right1 = (self._end - arcMid, arcMid)
            right2 = (self._mid, 0)
            right3 = (self._end, 0)
        else:
            left1 = (arcMid, arcMid)
            left2 = (self._mid, 0)
            left3 = (0, 0)
            right1 = (self._end - arcMid, self._end - arcMid)
            right2 = (self._mid, self._end)
            right3 = (self._end, self._end)

        return left0, left1, left2, left3, right0, right1, right2, right3

    def _get_twolines(self, tile_type: int) -> tuple[dw.Lines, dw.Lines]:
        left0, left1, left2, _, right0, right1, right2, _ = self._get_twoline_points(
            tile_type
        )
        lines_left = dw.Lines(
            *left0,
            *left1,
            *left2,
            stroke_width=self._line_width,
            stroke=self._line_color,
        )
        lines_right = dw.Lines(
            *right0,
            *right1,
            *right2,
            stroke_width=self._line_width,
            stroke=self._line_color,
        )

        return lines_left, lines_right

    def _get_hexagon_points(self, tile_type: int):
        p0 = (0, self._mid)
        p3 = (self._end, self._mid)

        if tile_type == 0:
            p1 = (self._mid, self._end)
            p2 = (self._end, self._end)
            p4 = (self._mid, 0)
            p5 = (0, 0)
        else:
            p1 = (0, self._end)
            p2 = (self._mid, self._end)
            p4 = (self._end, 0)
            p5 = (self._mid, 0)

        return (*p0, *p1, *p2, *p3, *p4, *p5)

    def _create_circle_pie(
        self,
        start: tuple[float, float],
        center: tuple[float, float],
        end: tuple[float, float],
        fill_color: str,
    ) -> dw.Path:
        r = self._mid
        pie = dw.Path(
            d=(
                f"M {start[0]} {start[1]}"
                f"A {r} {r} 0 0 0 {end[0]} {end[1]}"
                f"L {center[0]} {center[1]}"
                "Z"
            ),
            fill=fill_color,
        )
        return pie

    def _get_arc_points(self, tile_type: int):
        if tile_type == 1:
            left_start = (0, self._mid)
            left_center = (0, 0)
            left_end = (self._mid, 0)

            right_start = (self._end, self._mid)
            right_center = (self._end, self._end)
            right_end = (self._mid, self._end)
        else:
            left_start = (self._mid, self._end)
            left_center = (0, self._end)
            left_end = (0, self._mid)

            right_start = (self._mid, 0)
            right_center = (self._end, 0)
            right_end = (self._end, self._mid)

        return left_start, left_center, left_end, right_start, right_center, right_end

    def _get_octagon_points(self, tile_type: int) -> list[float]:
        points: list[tuple[float, float]] = [(0, 0)] * 8
        points[0] = (0, self._mid)
        points[2] = (self._mid, self._end)
        points[4] = (self._end, self._mid)
        points[6] = (self._mid, 0)

        arcMid = self._end * math.sqrt(2) / 4

        if tile_type == 0:
            points[1] = (arcMid, self._end - arcMid)
            points[3] = (self._end, self._end)
            points[5] = (self._end - arcMid, arcMid)
            points[7] = (0, 0)
        else:
            points[1] = (0, self._end)
            points[3] = (self._end - arcMid, self._end - arcMid)
            points[5] = (self._end, 0)
            points[7] = (arcMid, arcMid)

        unpacked_points: list[float] = []
        for point in points:
            unpacked_points.extend(point)

        return unpacked_points
