from collections import defaultdict
import math
from typing import Any

import drawsvg as dw  # type: ignore

from truchet_tiles.common.enum import SvgColors, Connector, Filledness


class RectTileGenerator(dict):
    def __init__(
        self,
        edge_length: int,
        max_line_width: int = 32,
        line_color: str = SvgColors.BLACK,
        fill_color: str = SvgColors.BLACK,
        bg_color: str = SvgColors.BLACK,
    ) -> None:
        assert edge_length > 0, "tile_size must be positive"
        self._end = edge_length
        self._mid = int(self._end / 2)
        self._max_line_width = max_line_width

        self._line_color = line_color
        self._fill_color = fill_color
        self._bg_color = bg_color

        self._bg_squares = self._get_bg_squares()

        self._base_tiles: dict[
            Filledness, dict[Connector, defaultdict[int, list[dw.Path]]]
        ] = {
            Filledness.linear: {
                # keys are line_width, values are list of svg elements
                Connector.straight: defaultdict(list),
                Connector.curved: defaultdict(list),
                Connector.twoline: defaultdict(list),
            },
            Filledness.filled: {
                # keys are line_width, values are list of svg elements
                Connector.straight: defaultdict(list),
                Connector.curved: defaultdict(list),
                Connector.twoline: defaultdict(list),
            },
        }

        for line_width in range(1, self._max_line_width + 1):
            self._create_linear_base_tiles(line_width)
            self._create_filled_base_tiles(line_width)

    def __getitem__(self, key: Any) -> Any:
        return self._base_tiles.__getitem__(key)

    def _get_bg_squares(self) -> dict[str, dw.Path]:
        bg_squares: dict[str, dw.Path] = {}
        r = self._end
        square_points = [0, 0, r, 0, r, r, 0, r]

        for color in (self._fill_color, self._bg_color):
            bg_squares[color] = dw.Lines(
                *square_points,
                fill=color,
                closed=True,
            )

        return bg_squares

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
        # Fill area out of diagonal lines
        self._create_outside_filled_straight_base_tile(0, line_width)
        self._create_outside_filled_straight_base_tile(1, line_width)

        # Fill area beween diagonal lines
        self._create_inside_filled_straight_base_tile(0, line_width)
        self._create_inside_filled_straight_base_tile(1, line_width)

    def _create_filled_curved_base_tiles(self, line_width: int):
        # Fill area outside of arc lines
        self._create_outside_filled_curved_base_tile(0, line_width)
        self._create_outside_filled_curved_base_tile(1, line_width)

        # Fill area between arc lines
        self._create_inside_filled_curved_base_tile(0, line_width)
        self._create_inside_filled_curved_base_tile(1, line_width)

    def _create_filled_twoline_base_tiles(self, line_width: int):
        # Fill area outside of arc lines
        self._create_outside_filled_twoline_base_tile(0, line_width)
        self._create_outside_filled_twoline_base_tile(1, line_width)

        # Fill area between arc lines
        self._create_inside_filled_twoline_base_tile(0, line_width)
        self._create_inside_filled_twoline_base_tile(1, line_width)

    # LEVEL 3 base tile functions
    def _get_lines(self, tile_type: int, line_width: int) -> tuple[dw.Line, dw.Line]:
        left1 = (0, self._mid)
        right1 = (self._end, self._mid)

        if tile_type == 0:
            left2 = (self._mid, self._end)
            right2 = (self._mid, 0)
        else:
            left2 = (self._mid, 0)
            right2 = (self._mid, self._end)

        line_left = dw.Line(
            *left1, *left2, stroke_width=line_width, stroke=self._line_color
        )
        line_right = dw.Line(
            *right1, *right2, stroke_width=line_width, stroke=self._line_color
        )
        return line_left, line_right

    def _create_linear_straight_base_tile(self, tile_type: int, line_width: int):
        ls = dw.Group(id=f"ls{tile_type}", fill="none")
        line_left, line_right = self._get_lines(tile_type, line_width)
        ls.append(line_left)
        ls.append(line_right)
        self._base_tiles[Filledness.linear][Connector.straight][line_width].append(ls)

    def _get_arcs(
        self,
        tile_type: int,
        line_width: int,
    ) -> tuple[dw.Arc, dw.Arc]:
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
            stroke_width=line_width,
            stroke=self._line_color,
        )

        curve_right = dw.Arc(
            *right_center,
            self._mid,
            *right_degrees,
            stroke_width=line_width,
            stroke=self._line_color,
        )

        return curve_left, curve_right

    def _create_linear_curved_base_tile(self, tile_type: int, line_width: int):
        lc = dw.Group(id=f"lc{tile_type}", fill="none")
        curve_left, curve_right = self._get_arcs(tile_type, line_width)
        lc.append(curve_left)
        lc.append(curve_right)
        self._base_tiles[Filledness.linear][Connector.curved][line_width].append(lc)

    def _get_twolines(
        self,
        tile_type: int,
        line_width: int,
    ) -> tuple[dw.Lines, dw.Lines]:
        left1 = (0, self._mid)
        right1 = (self._end, self._mid)
        arcMid = self._end * math.sqrt(2) / 4

        if tile_type == 0:
            leftM = (arcMid, self._end - arcMid)
            left2 = (self._mid, self._end)
            rightM = (self._end - arcMid, arcMid)
            right2 = (self._mid, 0)
        else:
            leftM = (arcMid, arcMid)
            left2 = (self._mid, 0)
            rightM = (self._end - arcMid, self._end - arcMid)
            right2 = (self._mid, self._end)

        lines_left = dw.Lines(
            *left1, *leftM, *left2, stroke_width=line_width, stroke=self._line_color
        )
        lines_right = dw.Lines(
            *right1, *rightM, *right2, stroke_width=line_width, stroke=self._line_color
        )

        return lines_left, lines_right

    def _create_linear_twoline_base_tile(self, tile_type: int, line_width: int):
        lt = dw.Group(id=f"lt{tile_type}", fill="none")
        lines_left, lines_right = self._get_twolines(tile_type, line_width)
        lt.append(lines_left)
        lt.append(lines_right)
        self._base_tiles[Filledness.linear][Connector.twoline][line_width].append(lt)

    def _create_outside_filled_straight_base_tile(
        self, tile_type: int, line_width: int
    ):
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

        fos = dw.Group(id=f"fos{tile_type}", fill="none")
        fos.append(self._bg_squares[self._bg_color])
        fos.append(triangle_left)
        fos.append(triangle_right)
        line_left, line_right = self._get_lines(tile_type, line_width)
        fos.append(line_left)
        fos.append(line_right)

        self._base_tiles[Filledness.filled][Connector.straight][line_width].append(fos)

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

    def _create_inside_filled_straight_base_tile(self, tile_type: int, line_width: int):
        hexagon_points = self._get_hexagon_points(tile_type)
        hexagon = dw.Lines(
            *hexagon_points,
            fill=self._fill_color,
            close=True,
        )

        fis = dw.Group(id=f"fis{tile_type}", fill="none")
        fis.append(self._bg_squares[self._bg_color])
        fis.append(hexagon)
        line_left, line_right = self._get_lines(tile_type, line_width)
        fis.append(line_left)
        fis.append(line_right)

        self._base_tiles[Filledness.filled][Connector.straight][line_width].append(fis)

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
                f"A {r} {r} 0 0 1 {end[0]} {end[1]}"
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

            right_start = (0, self._mid)
            right_center = (self._end, 0)
            right_end = (self._end, self._mid)

        return left_start, left_center, left_end, right_start, right_center, right_end

    def _create_outside_filled_curved_base_tile(self, tile_type: int, line_width: int):
        left_start, left_center, left_end, right_start, right_center, right_end = (
            self._get_arc_points(tile_type)
        )

        pie_left = self._create_circle_pie(
            left_start, left_center, left_end, self._fill_color
        )
        pie_right = self._create_circle_pie(
            right_start, right_center, right_end, self._fill_color
        )

        foc = dw.Group(id=f"foc{tile_type}", fill="none")
        foc.append(self._bg_squares[self._bg_color])
        foc.append(pie_left)
        foc.append(pie_right)
        curve_left, curve_right = self._get_arcs(tile_type, line_width)
        foc.append(curve_left)
        foc.append(curve_right)

        self._base_tiles[Filledness.filled][Connector.curved][line_width].append(foc)

    def _create_inside_filled_curved_base_tile(self, tile_type: int, line_width: int):
        left_start, left_center, left_end, right_start, right_center, right_end = (
            self._get_arc_points(tile_type)
        )

        pie_left = self._create_circle_pie(
            left_start, left_center, left_end, self._bg_color
        )
        pie_right = self._create_circle_pie(
            right_start, right_center, right_end, self._bg_color
        )

        fic = dw.Group(id=f"fic{tile_type}", fill="none")
        fic.append(self._bg_squares[self._fill_color])
        fic.append(pie_left)
        fic.append(pie_right)
        curve_left, curve_right = self._get_arcs(tile_type, line_width)
        fic.append(curve_left)
        fic.append(curve_right)

        self._base_tiles[Filledness.filled][Connector.curved][line_width].append(fic)

    def _create_outside_filled_twoline_base_tile(self, tile_type: int, line_width: int):
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

        fot = dw.Group(id=f"fot{tile_type}", fill="none")
        fot.append(self._bg_squares[self._bg_color])
        fot.append(poly_left)
        fot.append(poly_right)
        lines_left, lines_right = self._get_twolines(tile_type, line_width)
        fot.append(lines_left)
        fot.append(lines_right)

        self._base_tiles[Filledness.filled][Connector.twoline][line_width].append(fot)

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

    def _create_inside_filled_twoline_base_tile(self, tile_type: int, line_width: int):
        octagon_points = self._get_hexagon_points(tile_type)

        octagon = dw.Lines(
            *octagon_points,
            fill=self._fill_color,
            close=True,
        )

        fit = dw.Group(id=f"fit{tile_type}", fill="none")
        fit.append(self._bg_squares[self._bg_color])
        fit.append(octagon)
        lines_left, lines_right = self._get_twolines(tile_type, line_width)
        fit.append(lines_left)
        fit.append(lines_right)

        self._base_tiles[Filledness.filled][Connector.twoline][line_width].append(fit)
