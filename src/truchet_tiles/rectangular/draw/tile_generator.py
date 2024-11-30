from collections import defaultdict
import math
from typing import Any

import drawsvg as dw  # type: ignore

from truchet_tiles.common.enum import Colors, Connector, Filledness


class RectTileGenerator(dict):
    def __init__(self, tile_size: int, max_line_width: int = 32) -> None:
        assert tile_size > 0, "tile_size must be positive"
        self._end = tile_size
        self._mid = int(self._end / 2)
        self._max_line_width = max_line_width

        self._base_tiles: dict[
            Filledness, dict[Connector, defaultdict[int, list] | list]
        ] = {
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
        # Fill area out of diagonal lines
        self._create_outside_filled_straight_base_tile(0)
        self._create_outside_filled_straight_base_tile(1)

        # Fill area beween diagonal lines
        self._create_inside_filled_straight_base_tile(0)
        self._create_inside_filled_straight_base_tile(1)

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
    def _create_linear_straight_base_tile(self, tile_type: int, line_width: int):
        left1 = (0, self._mid)
        right1 = (self._end, self._mid)

        if tile_type == 0:
            left2 = (self._mid, self._end)
            right2 = (self._mid, 0)
        else:
            left2 = (self._mid, 0)
            right2 = (self._mid, self._end)

        line_left = dw.Line(
            *left1, *left2, stroke_width=line_width, stroke=Colors.SVG_BLACK
        )
        line_right = dw.Line(
            *right1, *right2, stroke_width=line_width, stroke=Colors.SVG_BLACK
        )

        ls = dw.Group(id=f"ls{tile_type}", fill="none")
        ls.append(line_left)
        ls.append(line_right)

        self._base_tiles[Filledness.linear][Connector.straight][line_width].append(ls)

    def _create_linear_curved_base_tile(self, tile_type: int, line_width: int):
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
            stroke=Colors.SVG_BLACK,
        )

        curve_right = dw.Arc(
            *right_center,
            self._mid,
            *right_degrees,
            stroke_width=line_width,
            stroke=Colors.SVG_BLACK,
        )

        lc = dw.Group(id=f"lc{tile_type}", fill="none")
        lc.append(curve_left)
        lc.append(curve_right)

        self._base_tiles[Filledness.linear][Connector.curved][line_width].append(lc)

    def _create_linear_twoline_base_tile(self, tile_type: int, line_width: int):
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
            *left1, *leftM, *left2, stroke_width=line_width, stroke=Colors.SVG_BLACK
        )
        lines_right = dw.Lines(
            *right1, *rightM, *right2, stroke_width=line_width, stroke=Colors.SVG_BLACK
        )

        lt = dw.Group(id=f"lt{tile_type}", fill="none")
        lt.append(lines_left)
        lt.append(lines_right)

        self._base_tiles[Filledness.linear][Connector.twoline][line_width].append(lt)

    def _create_outside_filled_straight_base_tile(self, tile_type: int):
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
            fill=Colors.SVG_BLACK,
            stroke=Colors.SVG_BLACK,
            close=True,
        )

        triangle_right = dw.Lines(
            *right0,
            *right1,
            *right2,
            fill=Colors.SVG_BLACK,
            stroke=Colors.SVG_BLACK,
            close=True,
        )

        fos = dw.Group(id=f"fos{tile_type}", fill="none")
        fos.append(triangle_left)
        fos.append(triangle_right)

        self._base_tiles[Filledness.filled][Connector.straight].append(fos)  # type: ignore

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

    def _create_inside_filled_straight_base_tile(self, tile_type: int):
        hexagon_points = self._get_hexagon_points(tile_type)

        hexagon = dw.Lines(
            *hexagon_points,
            fill=Colors.SVG_BLACK,
            stroke=Colors.SVG_BLACK,
            close=True,
        )

        fis = dw.Group(id=f"fis{tile_type}", fill="none")
        fis.append(hexagon)

        self._base_tiles[Filledness.filled][Connector.straight].append(fis)  # type: ignore

    def _create_outside_filled_curved_base_tile(self, tile_type: int):
        if tile_type == 1:
            left_center = (0, 0)
            right_center = (self._end, self._end)
        else:
            left_center = (0, self._end)
            right_center = (self._end, 0)

        pie_left = self._create_circle_pie(left_center)
        pie_right = self._create_circle_pie(right_center)

        foc = dw.Group(id=f"foc{tile_type}", fill="none")
        foc.append(pie_left)
        foc.append(pie_right)

        self._base_tiles[Filledness.filled][Connector.curved].append(foc)  # type: ignore

    def _create_inside_filled_curved_base_tile(self, tile_type: int):
        if tile_type == 1:
            la_center = (0, 0)
            ra_center = (self._end, self._end)
        else:
            la_center = (0, self._end)
            ra_center = (self._end, 0)

        pie_left = self._create_circle_pie(la_center, color=Colors.SVG_WHITE)
        pie_right = self._create_circle_pie(ra_center, color=Colors.SVG_WHITE)

        hexagon_points = self._get_hexagon_points(tile_type)
        black_hexagon = dw.Lines(
            *hexagon_points,
            stroke=Colors.SVG_BLACK,
            fill=Colors.SVG_BLACK,
            closed=True,
        )

        fic = dw.Group(id=f"fic{tile_type}", fill="none")
        fic.append(black_hexagon)
        fic.append(pie_left)
        fic.append(pie_right)

        self._base_tiles[Filledness.filled][Connector.curved].append(fic)  # type: ignore

    def _create_circle_pie(self, center: tuple[int, int], color=Colors.SVG_BLACK):
        pie = dw.Circle(
            *center,
            self._mid,
            fill=color,
            path_length=math.pi * self._mid / 2,
        )
        return pie

    def _create_outside_filled_twoline_base_tile(self, tile_type: int):
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
            fill=Colors.SVG_BLACK,
            stroke=Colors.SVG_BLACK,
            close=True,
        )

        poly_right = dw.Lines(
            *right0,
            *right1,
            *right2,
            *right3,
            fill=Colors.SVG_BLACK,
            stroke=Colors.SVG_BLACK,
            close=True,
        )

        fot = dw.Group(id=f"fot{tile_type}", fill="none")
        fot.append(poly_left)
        fot.append(poly_right)

        self._base_tiles[Filledness.filled][Connector.twoline].append(fot)  # type: ignore

    def _create_inside_filled_twoline_base_tile(self, tile_type: int):
        octagon_points = self._get_hexagon_points(tile_type)

        octagon = dw.Lines(
            *octagon_points,
            fill=Colors.SVG_BLACK,
            stroke=Colors.SVG_BLACK,
            close=True,
        )

        fit = dw.Group(id=f"fit{tile_type}", fill="none")
        fit.append(octagon)

        self._base_tiles[Filledness.filled][Connector.twoline].append(fit)  # type: ignore

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
