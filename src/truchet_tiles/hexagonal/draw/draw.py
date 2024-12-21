from collections import defaultdict
import drawsvg as dw  # type: ignore

from truchet_tiles.common.constants import ANIMATION_BEGIN, ANIMATION_DELAY
from truchet_tiles.common.enum import SvgColors, Connector
from truchet_tiles.hexagonal.draw.enum import HexAnimationMethod, HexTop
from truchet_tiles.hexagonal.draw.tile_generator import (
    create_inside_filled_curved_base_tile,
    create_inside_filled_line_base_tile,
    create_inside_filled_twoline_base_tile,
    create_outside_filled_curved_base_tile,
    create_outside_filled_line_base_tile,
    create_outside_filled_twoline_base_tile,
)
from truchet_tiles.hexagonal.hex_grid import (
    ORIENTATIONS,
    HexGrid,
    HexGridData,
    Layout,
    Point,
)


class HexTilingDrawer:
    tile_function_map = {
        (Connector.curved, 0): create_outside_filled_curved_base_tile,
        (Connector.curved, 1): create_inside_filled_curved_base_tile,
        (Connector.line, 0): create_outside_filled_line_base_tile,
        (Connector.line, 1): create_inside_filled_line_base_tile,
        (Connector.twoline, 0): create_outside_filled_twoline_base_tile,
        (Connector.twoline, 1): create_inside_filled_twoline_base_tile,
    }

    def __init__(
        self,
        dimension: int,
        grid: defaultdict[tuple[int, int], int],
        edge_length: float,
        flat_top: bool = False,
        connector: str = "twoline",
        hybrid_connector: str | None = None,
        animate: bool = False,
        animation_method: str = "at_once",
        animation_duration: float = 0.5,
        show_grid: bool = False,
        line_width: int = 1,
        grid_line_width: float = 0.5,
        line_color: str = SvgColors.BLACK,
        bg_color: str = SvgColors.WHITE,
        fill_color: str = SvgColors.BLACK,
        grid_color: str = SvgColors.RED,
    ) -> None:
        assert dimension > 0, "dimension must be positive"
        self._dimension = dimension
        assert edge_length > 0, "edge_length must be positive"
        self._edge_length = edge_length
        self._draw_size = 2 * (2 * self._dimension - 1) * self._edge_length

        self._orientation_name = HexTop.flat if flat_top else HexTop.pointy
        self._orientation = ORIENTATIONS[self._orientation_name]
        self._grid = grid
        self._hex_grid = self._calculate_hex_grid()

        self._line_width = line_width

        self._connector = Connector(connector)
        if hybrid_connector:
            self._hybrid_connector = Connector(hybrid_connector)
        else:
            self._hybrid_connector = self._connector

        self._show_grid_lines = show_grid
        self._grid_line_width = grid_line_width
        self._grid_color = grid_color

        self._line_color = line_color
        self._bg_color = bg_color
        self._fill_color = fill_color

        self._animate = animate
        self._animation_method = HexAnimationMethod(animation_method)
        self._animation_prev_grid = {
            key: 0 for key in grid
        }  # TODO: Add hex grid version.
        self._animation_duration = animation_duration

        self._svg = dw.Drawing(
            self._draw_size,
            self._draw_size,
            origin=(0, 0),
            id_prefix="hex_truchet_tiling",
        )
        self._svg_top_group = dw.Group(
            id="truchet_group", fill="none"
        )  # To handle translations

    def _calculate_hex_grid(self) -> HexGrid:
        layout = Layout(
            orientation=self._orientation,
            size=Point(self._edge_length, self._edge_length),
            origin=Point(0, 0),
        )

        return HexGrid(dimension=self._dimension, hex_grid=self._grid, layout=layout)

    @property
    def svg(self):
        return self._svg

    def draw(self):
        self._clear_screan()
        self._draw()

        if self._show_grid_lines:
            self._draw_grid_lines()

        self._update_svg()

    def _clear_screan(self):
        self._svg.clear()
        self._svg = dw.Drawing(
            self._draw_size, self._draw_size, id_prefix="truchet_tiling"
        )
        self._svg_top_group = dw.Group(id="truchet_group", fill="none")

    def _update_svg(self):
        self._svg.view_box = (
            -self._draw_size / 2,
            -self._draw_size / 2,
            self._draw_size,
            self._draw_size,
        )

        self._svg.set_render_size()
        self._svg.append(dw.Use(self._svg_top_group, 0, 0, transform="scale(1.1)"))

    def _draw(self):
        anim_start = ANIMATION_BEGIN
        hex_index = 0

        for hex_, hex_data in self._hex_grid.items():
            coord = (hex_.q, hex_.r)
            animate = self._animate and (
                self._animation_prev_grid[coord] != self._grid[coord]
            )

            if animate:
                if self._animation_method == HexAnimationMethod.by_tile:
                    anim_start = ANIMATION_BEGIN + hex_index * self._animation_duration
                elif self._animation_method == HexAnimationMethod.by_ring:
                    anim_start = ANIMATION_BEGIN + abs(hex_) * self._animation_duration
                elif self._animation_method == HexAnimationMethod.at_once:
                    anim_start = ANIMATION_BEGIN

            used_tile = self._get_tile(hex_data, anim_start, animate)

            if animate:
                self._append_rotation(hex_data, used_tile, anim_start)

            self._svg_top_group.append(used_tile)
            hex_index += 1

    def _append_rotation(
        self, hex_data: HexGridData, used_tile: dw.Use, anim_start: float
    ):
        def _get_rotation(begin, dur, start_deg, end_deg):
            return dw.AnimateTransform(
                attributeName="transform",
                begin=begin,
                dur=dur,
                type="rotate",
                from_or_values=f"{start_deg} {hex_data.center.x} {hex_data.center.y}",
                to=f"{end_deg} {hex_data.center.x} {hex_data.center.y}",
                fill="freeze",
                repeatCount="1",
            )

        # The following animation will make the svg appear to start from the prev state
        used_tile.append_anim(_get_rotation(ANIMATION_DELAY, ANIMATION_DELAY, 0, 60))
        used_tile.append_anim(
            _get_rotation(anim_start, self._animation_duration, 60, 120)
        )

    def _get_tile(self, hex_data: HexGridData, anim_start: float, animate: bool):
        connector = self._connector if hex_data.value == 0 else self._hybrid_connector
        func = self.tile_function_map[(connector, hex_data.value)]

        base_tile = func(
            self._edge_length,
            self._orientation_name,
            self._line_width,
            self._line_color,
            self._fill_color,
            self._bg_color,
            animate,
            anim_start,
            self._animation_duration,
        )
        return dw.Use(base_tile, hex_data.center.x, hex_data.center.y)

    def _draw_grid_lines(self):
        for hex_data in self._hex_grid.values():
            points = []
            for p in hex_data.corners:
                points += [p.x, p.y]

            self._svg_top_group.append(
                dw.Lines(
                    *points,
                    stroke=self._grid_color,
                    stroke_width=self._grid_line_width,
                    close=True,
                )
            )
