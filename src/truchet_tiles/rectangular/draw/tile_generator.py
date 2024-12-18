from functools import cache
import math
import drawsvg as dw  # type: ignore

from truchet_tiles.common.constants import ANIMATION_DELAY


# Helper functions
def _get_bg_square(color: str, edge_length: float) -> dw.Lines:
    square_points = [0, 0, edge_length, 0, edge_length, edge_length, 0, edge_length]
    return dw.Lines(
        *square_points,
        fill=color,
        close=True,
    )


def _get_line_points(tile_type: int, edge_length: float):
    edge_mid = edge_length / 2

    left0 = (0.0, edge_mid)
    right0 = (edge_length, edge_mid)

    if tile_type == 0:
        left1 = (edge_mid, edge_length)
        left2 = (0.0, edge_length)
        right1 = (edge_mid, 0.0)
        right2 = (edge_length, 0.0)
    else:
        left1 = (edge_mid, 0.0)
        left2 = (0.0, 0.0)
        right1 = (edge_mid, edge_length)
        right2 = (edge_length, edge_length)

    return left0, left1, left2, right0, right1, right2


def _get_lines(
    tile_type: int, edge_length: float, line_width: int, line_color: str
) -> tuple[dw.Line, dw.Line]:
    left0, left1, _, right0, right1, _ = _get_line_points(tile_type, edge_length)

    line_left = dw.Line(*left0, *left1, stroke_width=line_width, stroke=line_color)
    line_right = dw.Line(*right0, *right1, stroke_width=line_width, stroke=line_color)
    return line_left, line_right


def _get_hexagon_points(tile_type: int, edge_length: float):
    mid = edge_length / 2

    p0 = (0.0, mid)
    p3 = (edge_length, mid)

    if tile_type == 0:
        p1 = (mid, edge_length)
        p2 = (edge_length, edge_length)
        p4 = (mid, 0.0)
        p5 = (0.0, 0.0)
    else:
        p1 = (0, edge_length)
        p2 = (mid, edge_length)
        p4 = (edge_length, 0.0)
        p5 = (mid, 0.0)

    return (*p0, *p1, *p2, *p3, *p4, *p5)


def _get_arc_points(tile_type: int, edge_length: float):
    mid = edge_length / 2

    if tile_type == 1:
        left_start = (0.0, mid)
        left_center = (0.0, 0.0)
        left_end = (mid, 0.0)

        right_start = (edge_length, mid)
        right_center = (edge_length, edge_length)
        right_end = (mid, edge_length)
    else:
        left_start = (mid, edge_length)
        left_center = (0.0, edge_length)
        left_end = (0.0, mid)

        right_start = (mid, 0.0)
        right_center = (edge_length, 0.0)
        right_end = (edge_length, mid)

    return left_start, left_center, left_end, right_start, right_center, right_end


def _create_circle_pie(
    edge_length: float,
    start: tuple[float, float],
    center: tuple[float, float],
    end: tuple[float, float],
    fill_color: str,
) -> dw.Path:
    r = edge_length / 2
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


def _get_arcs(
    tile_type: int, edge_length: float, line_width: int, line_color: str
) -> tuple[dw.Arc, dw.Arc]:
    mid = edge_length / 2
    edge_length = edge_length

    if tile_type == 1:
        left_center = (0.0, 0.0)
        left_degrees = (90.0, 0.0)
        right_center = (edge_length, edge_length)
        right_degrees = (270.0, 180.0)
    else:
        left_center = (0.0, edge_length)
        left_degrees = (360.0, 270.0)
        right_center = (edge_length, 0.0)
        right_degrees = (180.0, 90.0)

    curve_left = dw.Arc(
        *left_center,
        mid,
        *left_degrees,
        stroke_width=line_width,
        stroke=line_color,
    )
    curve_right = dw.Arc(
        *right_center,
        mid,
        *right_degrees,
        stroke_width=line_width,
        stroke=line_color,
    )

    return curve_left, curve_right


def _get_twoline_points(tile_type: int, edge_length: float):
    mid = edge_length / 2

    left0 = (0.0, mid)
    right0 = (edge_length, mid)
    arcMid = edge_length * math.sqrt(2) / 4

    if tile_type == 0:
        left1 = (arcMid, edge_length - arcMid)
        left2 = (mid, edge_length)
        left3 = (0.0, edge_length)
        right1 = (edge_length - arcMid, arcMid)
        right2 = (mid, 0.0)
        right3 = (edge_length, 0.0)
    else:
        left1 = (arcMid, arcMid)
        left2 = (mid, 0.0)
        left3 = (0.0, 0.0)
        right1 = (edge_length - arcMid, edge_length - arcMid)
        right2 = (mid, edge_length)
        right3 = (edge_length, edge_length)

    return left0, left1, left2, left3, right0, right1, right2, right3


def _get_twolines(
    tile_type: int, edge_length: float, line_width: int, line_color: str
) -> tuple[dw.Lines, dw.Lines]:
    left0, left1, left2, _, right0, right1, right2, _ = _get_twoline_points(
        tile_type, edge_length
    )
    lines_left = dw.Lines(
        *left0,
        *left1,
        *left2,
        stroke_width=line_width,
        stroke=line_color,
    )
    lines_right = dw.Lines(
        *right0,
        *right1,
        *right2,
        stroke_width=line_width,
        stroke=line_color,
    )

    return lines_left, lines_right


def _get_octagon_points(tile_type: int, edge_length: float) -> list[float]:
    mid = edge_length / 2

    points: list[tuple[float, float]] = [(0, 0)] * 8
    points[0] = (0, mid)
    points[2] = (mid, edge_length)
    points[4] = (edge_length, mid)
    points[6] = (mid, 0)

    arcMid = edge_length * math.sqrt(2) / 4

    if tile_type == 0:
        points[1] = (arcMid, edge_length - arcMid)
        points[3] = (edge_length, edge_length)
        points[5] = (edge_length - arcMid, arcMid)
        points[7] = (0, 0)
    else:
        points[1] = (0, edge_length)
        points[3] = (edge_length - arcMid, edge_length - arcMid)
        points[5] = (edge_length, 0)
        points[7] = (arcMid, arcMid)

    unpacked_points: list[float] = []
    for point in points:
        unpacked_points.extend(point)

    return unpacked_points


def _append_color_fade(
    element: dw.Path, from_color: str, to_color: str, anim_start: float, anim_dur: float
):
    def _get_color_fade(begin, dur, start, end):
        return dw.Animate(
            attributeName="fill",
            begin=begin,
            dur=dur,
            from_or_values=f"{start};{end}",
            fill="freeze",
            repeatCount="1",
        )

    element.append_anim(
        _get_color_fade(ANIMATION_DELAY, ANIMATION_DELAY, to_color, from_color)
    )
    element.append_anim(_get_color_fade(anim_start, anim_dur, from_color, to_color))


# Tile generation functions
@cache
def create_outside_filled_line_base_tile(
    tile_type: int,
    edge_length: float,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
) -> dw.Group:
    ofl = dw.Group(fill="none")
    bg_square = _get_bg_square(bg_color, edge_length)
    if animate_colors:
        _append_color_fade(bg_square, fill_color, bg_color, anim_start, anim_dur)

    ofl.append(bg_square)

    left0, left1, left2, right0, right1, right2 = _get_line_points(
        tile_type, edge_length
    )
    triangle_left = dw.Lines(
        *left0,
        *left1,
        *left2,
        fill=fill_color,
        close=True,
    )
    triangle_right = dw.Lines(
        *right0,
        *right1,
        *right2,
        fill=fill_color,
        close=True,
    )
    if animate_colors:
        _append_color_fade(triangle_left, bg_color, fill_color, anim_start, anim_dur)
        _append_color_fade(triangle_right, bg_color, fill_color, anim_start, anim_dur)

    ofl.append(triangle_left)
    ofl.append(triangle_right)

    line_left, line_right = _get_lines(tile_type, edge_length, line_width, line_color)
    ofl.append(line_left)
    ofl.append(line_right)

    return ofl


@cache
def create_inside_filled_line_base_tile(
    tile_type: int,
    edge_length: float,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
) -> dw.Group:
    ifl = dw.Group(fill="none")
    bg_square = _get_bg_square(bg_color, edge_length)
    if animate_colors:
        _append_color_fade(bg_square, fill_color, bg_color, anim_start, anim_dur)

    ifl.append(bg_square)

    hexagon_points = _get_hexagon_points(tile_type, edge_length)
    hexagon = dw.Lines(
        *hexagon_points,
        fill=fill_color,
        close=True,
    )
    if animate_colors:
        _append_color_fade(hexagon, bg_color, fill_color, anim_start, anim_dur)

    ifl.append(hexagon)

    line_left, line_right = _get_lines(tile_type, edge_length, line_width, line_color)
    ifl.append(line_left)
    ifl.append(line_right)

    return ifl


@cache
def create_outside_filled_curved_base_tile(
    tile_type: int,
    edge_length: float,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
) -> dw.Group:
    ofc = dw.Group(fill="none")
    bg_square = _get_bg_square(bg_color, edge_length)
    if animate_colors:
        _append_color_fade(bg_square, fill_color, bg_color, anim_start, anim_dur)

    ofc.append(bg_square)

    left_start, left_center, left_end, right_start, right_center, right_end = (
        _get_arc_points(tile_type, edge_length)
    )
    pie_left = _create_circle_pie(
        edge_length, left_start, left_center, left_end, fill_color
    )
    pie_right = _create_circle_pie(
        edge_length, right_start, right_center, right_end, fill_color
    )
    if animate_colors:
        _append_color_fade(pie_left, bg_color, fill_color, anim_start, anim_dur)
        _append_color_fade(pie_right, bg_color, fill_color, anim_start, anim_dur)

    ofc.append(pie_left)
    ofc.append(pie_right)

    curve_left, curve_right = _get_arcs(tile_type, edge_length, line_width, line_color)
    ofc.append(curve_left)
    ofc.append(curve_right)

    return ofc


@cache
def create_inside_filled_curved_base_tile(
    tile_type: int,
    edge_length: float,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
) -> dw.Group:
    ifc = dw.Group(fill="none")
    bg_square = _get_bg_square(fill_color, edge_length)
    if animate_colors:
        _append_color_fade(bg_square, bg_color, fill_color, anim_start, anim_dur)

    ifc.append(bg_square)

    left_start, left_center, left_end, right_start, right_center, right_end = (
        _get_arc_points(tile_type, edge_length)
    )
    pie_left = _create_circle_pie(
        edge_length, left_start, left_center, left_end, bg_color
    )
    pie_right = _create_circle_pie(
        edge_length, right_start, right_center, right_end, bg_color
    )
    if animate_colors:
        _append_color_fade(pie_left, fill_color, bg_color, anim_start, anim_dur)
        _append_color_fade(pie_right, fill_color, bg_color, anim_start, anim_dur)

    ifc.append(pie_left)
    ifc.append(pie_right)

    curve_left, curve_right = _get_arcs(tile_type, edge_length, line_width, line_color)
    ifc.append(curve_left)
    ifc.append(curve_right)

    return ifc


@cache
def create_outside_filled_twoline_base_tile(
    tile_type: int,
    edge_length: float,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
):
    oft = dw.Group(fill="none")
    bg_square = _get_bg_square(bg_color, edge_length)
    if animate_colors:
        _append_color_fade(bg_square, fill_color, bg_color, anim_start, anim_dur)

    oft.append(bg_square)

    left0, left1, left2, left3, right0, right1, right2, right3 = _get_twoline_points(
        tile_type, edge_length
    )
    poly_left = dw.Lines(
        *left0,
        *left1,
        *left2,
        *left3,
        fill=fill_color,
        close=True,
    )
    poly_right = dw.Lines(
        *right0,
        *right1,
        *right2,
        *right3,
        fill=fill_color,
        close=True,
    )
    if animate_colors:
        _append_color_fade(poly_left, bg_color, fill_color, anim_start, anim_dur)
        _append_color_fade(poly_right, bg_color, fill_color, anim_start, anim_dur)

    oft.append(poly_left)
    oft.append(poly_right)

    lines_left, lines_right = _get_twolines(
        tile_type, edge_length, line_width, line_color
    )
    oft.append(lines_left)
    oft.append(lines_right)

    return oft


@cache
def create_inside_filled_twoline_base_tile(
    tile_type: int,
    edge_length: float,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
):
    ift = dw.Group(fill="none")
    bg_square = _get_bg_square(bg_color, edge_length)
    if animate_colors:
        _append_color_fade(bg_square, fill_color, bg_color, anim_start, anim_dur)

    ift.append(bg_square)

    octagon_points = _get_octagon_points(tile_type, edge_length)
    octagon = dw.Lines(
        *octagon_points,
        fill=fill_color,
        close=True,
    )
    ift.append(octagon)
    if animate_colors:
        _append_color_fade(octagon, bg_color, fill_color, anim_start, anim_dur)

    lines_left, lines_right = _get_twolines(
        tile_type, edge_length, line_width, line_color
    )
    ift.append(lines_left)
    ift.append(lines_right)

    return ift
