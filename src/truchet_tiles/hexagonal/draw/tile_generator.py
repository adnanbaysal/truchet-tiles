from functools import cache

import drawsvg as dw  # type: ignore

from truchet_tiles.common.constants import ANIMATION_DELAY
from truchet_tiles.hexagonal.draw.enum import HexTop
from truchet_tiles.hexagonal.hex_grid import (
    Hex,
    HexGeometry,
    Layout,
    ORIENTATIONS,
    Point,
)


# Helper functions
@cache
def _get_hex_geometry(hex_top: HexTop, edge_length: float) -> HexGeometry:
    orientation = ORIENTATIONS[hex_top]
    layout = Layout(
        orientation=orientation,
        size=Point(edge_length, edge_length),
        origin=Point(0, 0),
    )
    return HexGeometry(layout, Hex(0, 0, 0))


def _get_bg_hexagon(color: str, hex_geometry: HexGeometry) -> dw.Path:
    hexagon_corners = []
    for p in hex_geometry.corners:
        hexagon_corners += [p.x, p.y]

    return dw.Lines(
        *hexagon_corners,
        fill=color,
        closed=True,
    )


def _get_lines(
    tile_type: int, hex_geometry: HexGeometry, line_width: int, line_color: str
) -> list[dw.Line]:
    return [
        dw.Line(
            hex_geometry.edge_mids[2 * i + tile_type].x,
            hex_geometry.edge_mids[2 * i + tile_type].y,
            hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x,
            hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y,
            stroke_width=line_width,
            stroke=line_color,
        )
        for i in range(3)
    ]


def _get_arcs(
    tile_type: int,
    hex_geometry: HexGeometry,
    line_width: int,
    line_color: str,
    edge_length: float,
) -> list[dw.Path]:
    return [
        dw.Path(
            d=(
                f"M {hex_geometry.edge_mids[2 * i + tile_type].x} "
                f"{hex_geometry.edge_mids[2 * i + tile_type].y} "
                f"A {edge_length / 2} {edge_length / 2} 0 0 1 "
                f"{hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].x} "
                f"{hex_geometry.edge_mids[(2 * i + 1 + tile_type) % 6].y}"
            ),
            stroke_width=line_width,
            stroke=line_color,
        )
        for i in range(3)
    ]


def _get_twolines(
    tile_type: int, hex_geometry: HexGeometry, line_width: int, line_color: str
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
            stroke=line_color,
        )
        for i in range(3)
    ]


def _create_circle_pie(
    start: tuple[float, float],
    center: tuple[float, float],
    end: tuple[float, float],
    fill_color: str,
    edge_length: float,
) -> dw.Path:
    r = edge_length / 2
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


# TODO: Put this to common code
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
    edge_length: int,
    hex_top: HexTop,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
) -> dw.Group:
    hex_geometry = _get_hex_geometry(hex_top, edge_length)
    lines = _get_lines(0, hex_geometry, line_width, line_color)
    triangles = [
        dw.Lines(
            hex_geometry.edge_mids[2 * i].x,
            hex_geometry.edge_mids[2 * i].y,
            hex_geometry.corners[(2 * i + 1) % 6].x,
            hex_geometry.corners[(2 * i + 1) % 6].y,
            hex_geometry.edge_mids[(2 * i + 1) % 6].x,
            hex_geometry.edge_mids[(2 * i + 1) % 6].y,
            fill=fill_color,
            close=True,
        )
        for i in range(3)
    ]

    ofl = dw.Group(fill="none")

    bg_hexagon = _get_bg_hexagon(bg_color, hex_geometry)

    if animate_colors:
        _append_color_fade(bg_hexagon, fill_color, bg_color, anim_start, anim_dur)
        for i in range(3):
            _append_color_fade(triangles[i], bg_color, fill_color, anim_start, anim_dur)

    ofl.append(bg_hexagon)
    for i in range(3):
        ofl.append(triangles[i])
    for i in range(3):
        ofl.append(lines[i])

    return ofl


@cache
def create_inside_filled_line_base_tile(
    edge_length: int,
    hex_top: HexTop,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
) -> dw.Group:
    hex_geometry = _get_hex_geometry(hex_top, edge_length)
    lines = _get_lines(0, hex_geometry, line_width, line_color)

    points = []
    for i in range(3):
        points += [
            hex_geometry.edge_mids[2 * i + 1].x,
            hex_geometry.edge_mids[2 * i + 1].y,
            hex_geometry.edge_mids[(2 * i + 2) % 6].x,
            hex_geometry.edge_mids[(2 * i + 2) % 6].y,
            hex_geometry.corners[(2 * i + 3) % 6].x,
            hex_geometry.corners[(2 * i + 3) % 6].y,
        ]

    polygon = dw.Lines(*points, fill=fill_color, close=True)

    ifl = dw.Group(fill="none")

    bg_hexagon = _get_bg_hexagon(bg_color, hex_geometry)

    if animate_colors:
        _append_color_fade(bg_hexagon, fill_color, bg_color, anim_start, anim_dur)
        _append_color_fade(polygon, bg_color, fill_color, anim_start, anim_dur)

    ifl.append(bg_hexagon)
    ifl.append(polygon)
    for i in range(3):
        ifl.append(lines[i])

    return ifl


@cache
def create_outside_filled_curved_base_tile(
    edge_length: int,
    hex_top: HexTop,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
) -> dw.Group:
    hex_geometry = _get_hex_geometry(hex_top, edge_length)

    arcs = _get_arcs(0, hex_geometry, line_width, line_color, edge_length)
    pies = [
        _create_circle_pie(
            start=(
                hex_geometry.edge_mids[(2 * i) % 6].x,
                hex_geometry.edge_mids[(2 * i) % 6].y,
            ),
            center=(
                hex_geometry.corners[(2 * i + 1) % 6].x,
                hex_geometry.corners[(2 * i + 1) % 6].y,
            ),
            end=(
                hex_geometry.edge_mids[(2 * i + 1) % 6].x,
                hex_geometry.edge_mids[(2 * i + 1) % 6].y,
            ),
            fill_color=fill_color,
            edge_length=edge_length,
        )
        for i in range(3)
    ]

    bg_hexagon = _get_bg_hexagon(bg_color, hex_geometry)

    if animate_colors:
        _append_color_fade(bg_hexagon, fill_color, bg_color, anim_start, anim_dur)
        for i in range(3):
            _append_color_fade(pies[i], bg_color, fill_color, anim_start, anim_dur)

    ofc = dw.Group(fill="none")

    ofc.append(bg_hexagon)
    for i in range(3):
        ofc.append(pies[i])
    for i in range(3):
        ofc.append(arcs[i])

    return ofc


@cache
def create_inside_filled_curved_base_tile(
    edge_length: int,
    hex_top: HexTop,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
) -> dw.Group:
    hex_geometry = _get_hex_geometry(hex_top, edge_length)

    arcs = _get_arcs(1, hex_geometry, line_width, line_color, edge_length)
    pies = [
        _create_circle_pie(
            start=(
                hex_geometry.edge_mids[(2 * i + 1) % 6].x,
                hex_geometry.edge_mids[(2 * i + 1) % 6].y,
            ),
            center=(
                hex_geometry.corners[(2 * i + 2) % 6].x,
                hex_geometry.corners[(2 * i + 2) % 6].y,
            ),
            end=(
                hex_geometry.edge_mids[(2 * i + 2) % 6].x,
                hex_geometry.edge_mids[(2 * i + 2) % 6].y,
            ),
            fill_color=bg_color,
            edge_length=edge_length,
        )
        for i in range(3)
    ]

    bg_hexagon = _get_bg_hexagon(fill_color, hex_geometry)

    if animate_colors:
        _append_color_fade(bg_hexagon, bg_color, fill_color, anim_start, anim_dur)
        for i in range(3):
            _append_color_fade(pies[i], fill_color, bg_color, anim_start, anim_dur)

    ifc = dw.Group(fill="none")
    ifc.append(bg_hexagon)
    for i in range(3):
        ifc.append(pies[i])
    for i in range(3):
        ifc.append(arcs[i])

    return ifc


@cache
def create_outside_filled_twoline_base_tile(
    edge_length: int,
    hex_top: HexTop,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
) -> dw.Group:
    hex_geometry = _get_hex_geometry(hex_top, edge_length)

    twolines = _get_twolines(0, hex_geometry, line_width, line_color)
    parallelograms = [
        dw.Lines(
            hex_geometry.edge_mids[2 * i].x,
            hex_geometry.edge_mids[2 * i].y,
            hex_geometry.corners[(2 * i + 1) % 6].x,
            hex_geometry.corners[(2 * i + 1) % 6].y,
            hex_geometry.edge_mids[(2 * i + 1) % 6].x,
            hex_geometry.edge_mids[(2 * i + 1) % 6].y,
            hex_geometry.half_hex_corners[(2 * i + 1) % 6].x,
            hex_geometry.half_hex_corners[(2 * i + 1) % 6].y,
            fill=fill_color,
            close=True,
        )
        for i in range(3)
    ]

    bg_hexagon = _get_bg_hexagon(bg_color, hex_geometry)

    if animate_colors:
        _append_color_fade(bg_hexagon, fill_color, bg_color, anim_start, anim_dur)
        for i in range(3):
            _append_color_fade(
                parallelograms[i], bg_color, fill_color, anim_start, anim_dur
            )

    oft = dw.Group(fill="none")
    oft.append(bg_hexagon)
    for i in range(3):
        oft.append(parallelograms[i])
    for i in range(3):
        oft.append(twolines[i])

    return oft


@cache
def create_inside_filled_twoline_base_tile(
    edge_length: int,
    hex_top: HexTop,
    line_width: int,
    line_color: str,
    fill_color: str,
    bg_color: str,
    animate_colors: bool,
    anim_start: float,
    anim_dur: float,
) -> dw.Group:
    hex_geometry = _get_hex_geometry(hex_top, edge_length)

    twolines = _get_twolines(1, hex_geometry, line_width, line_color)
    points = []
    for i in range(3):
        points += [
            hex_geometry.edge_mids[2 * i + 1].x,
            hex_geometry.edge_mids[2 * i + 1].y,
            hex_geometry.half_hex_corners[(2 * i + 2) % 6].x,
            hex_geometry.half_hex_corners[(2 * i + 2) % 6].y,
            hex_geometry.edge_mids[(2 * i + 2) % 6].x,
            hex_geometry.edge_mids[(2 * i + 2) % 6].y,
            hex_geometry.corners[(2 * i + 3) % 6].x,
            hex_geometry.corners[(2 * i + 3) % 6].y,
        ]

    polygon = dw.Lines(*points, fill=fill_color, close=True)
    bg_hexagon = _get_bg_hexagon(bg_color, hex_geometry)

    if animate_colors:
        _append_color_fade(bg_hexagon, fill_color, bg_color, anim_start, anim_dur)
        _append_color_fade(polygon, bg_color, fill_color, anim_start, anim_dur)

    ift = dw.Group(fill="none")
    ift.append(bg_hexagon)
    ift.append(polygon)
    for i in range(3):
        ift.append(twolines[i])

    return ift
