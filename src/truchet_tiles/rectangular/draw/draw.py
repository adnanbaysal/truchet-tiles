from collections import defaultdict
import drawsvg as dw  # type: ignore

from truchet_tiles.common.constants import ANIMATION_BEGIN, ANIMATION_DELAY
from truchet_tiles.common.enum import SvgColors, Connector
from truchet_tiles.rectangular.draw.enum import (
    RectAnimationMethod,
    AxisAlignment,
)
from truchet_tiles.rectangular.draw.tile_generator import (
    create_inside_filled_curved_base_tile,
    create_inside_filled_line_base_tile,
    create_inside_filled_twoline_base_tile,
    create_outside_filled_curved_base_tile,
    create_outside_filled_line_base_tile,
    create_outside_filled_twoline_base_tile,
)


class RectTilingDrawer:
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
        align_to_axis: bool = False,
        connector: str = "line",
        hybrid_connector: str | None = None,
        animate: bool = False,
        animation_duration: float = 1.0,
        animation_method: str = "at_once",
        show_grid: bool = False,
        line_width: int = 1,
        grid_line_width: float = 0.5,
        line_color: str = SvgColors.BLACK,
        bg_color: str = SvgColors.WHITE,
        fill_color: str = SvgColors.BLACK,
        grid_color: str = SvgColors.RED,
    ) -> None:
        self._grid: defaultdict[tuple[int, int], int] = grid

        assert edge_length > 0, "eldge_length must be positive"
        self._edge_length = edge_length
        self._edge_mid = self._edge_length / 2
        self._dimension = dimension
        self._draw_size = self._dimension * self._edge_length

        self._line_width = line_width

        self._connector = Connector(connector)
        if hybrid_connector:
            self._hybrid_connector = Connector(hybrid_connector)
        else:
            self._hybrid_connector = self._connector

        self._alignment_style = (
            AxisAlignment.aligned if align_to_axis else AxisAlignment.rotated
        )

        self._show_grid_lines = show_grid
        self._grid_line_width = grid_line_width
        self._grid_color = grid_color

        self._line_color = line_color
        self._bg_color = bg_color
        self._fill_color = fill_color

        self._animate = animate
        self._animation_method = RectAnimationMethod(animation_method)
        self._animation_prev_grid: defaultdict[tuple[int, int], int] = defaultdict(int)
        self._animation_duration = animation_duration

        self._svg = dw.Drawing(
            self._draw_size, self._draw_size, id_prefix="rect_truchet_tiling"
        )
        self._svg_top_group = dw.Group(
            id="truchet_group", fill="none"
        )  # To handle translations

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

    def _get_transform(self):
        return (
            f"matrix(.5 -.5 .5 .5 0 {self._edge_length * self._dimension / 2})"
            if self._alignment_style == AxisAlignment.aligned
            else None
        )

    def _update_svg(self):
        kwargs = {}
        transform = self._get_transform()

        if transform:
            kwargs["transform"] = transform
            self._svg.view_box = (
                self._draw_size / 4,
                self._draw_size / 4,
                self._draw_size / 2,
                self._draw_size / 2,
            )

        self._svg.set_render_size()
        self._svg.append(dw.Use(self._svg_top_group, 0, 0, **kwargs))

    def _draw(self):
        anim_start = ANIMATION_BEGIN
        grid_of_fill_inside = self._generate_fill_inside_grid()

        for row in range(self._dimension):
            y_offset = row * self._edge_length
            for col in range(self._dimension):
                x_offset = col * self._edge_length

                tile_type = self._grid[(row, col)]
                inside_filled = grid_of_fill_inside[(row, col)]

                animate = self._animate and (
                    self._animation_prev_grid[(row, col)] != self._grid[(row, col)]
                )

                used_tile = self._get_tile(
                    x_offset,
                    y_offset,
                    tile_type,
                    inside_filled,
                    anim_start,
                    animate,
                )

                if animate:
                    self._append_rotation(row, col, used_tile, anim_start)

                self._svg_top_group.append(used_tile)

                if self._animation_method == RectAnimationMethod.by_tile:
                    if self._grid[(row, col)] != self._animation_prev_grid[(row, col)]:
                        anim_start += self._animation_duration

            if self._animation_method == RectAnimationMethod.by_row:
                anim_start += self._animation_duration

    def _append_rotation(
        self, row: int, col: int, used_tile: dw.Use, anim_start: float
    ):
        x_offset = col * self._edge_length
        y_offset = row * self._edge_length

        def _get_rotation(begin, dur, start_deg, end_deg):
            return dw.AnimateTransform(
                attributeName="transform",
                begin=begin,
                dur=dur,
                type="rotate",
                from_or_values=f"{start_deg} {x_offset + self._edge_mid} {y_offset + self._edge_mid}",
                to=f"{end_deg} {x_offset + self._edge_mid} {y_offset + self._edge_mid}",
                fill="freeze",
                repeatCount="1",
            )

        # The following animation will make the svg appear to start from the prev state
        used_tile.append_anim(_get_rotation(ANIMATION_DELAY, ANIMATION_DELAY, 0, 90))
        used_tile.append_anim(
            _get_rotation(anim_start, self._animation_duration, 90, 180)
        )

    def _generate_fill_inside_grid(self) -> defaultdict[tuple[int, int], int]:
        fill_inside_grid: defaultdict[tuple[int, int], int] = defaultdict(int)
        for grid_row in range(self._dimension):
            for grid_col in range(self._dimension):
                neighbor = self._neighbor_cell(self._grid, grid_row, grid_col)
                bit_changed = self._grid[(grid_row, grid_col)] ^ neighbor
                if grid_row == 0 and grid_col == 0:
                    neighbor_fill = self._grid[(0, 0)]
                else:
                    neighbor_fill = self._neighbor_cell(
                        fill_inside_grid, grid_row, grid_col
                    )
                fill_inside_grid[(grid_row, grid_col)] = neighbor_fill ^ bit_changed ^ 1

        return fill_inside_grid

    @staticmethod
    def _neighbor_cell(_grid: dict[tuple[int, int], int], row: int, col: int) -> int:
        if row == 0 and col == 0:
            return _grid[(row, col)]
        if col > 0:
            return _grid[(row, col - 1)]
        if row > 0:
            return _grid[(row - 1, col)]
        raise ValueError("Invalid row and column")

    def _get_tile(
        self,
        x_offset: int,
        y_offset: int,
        tile_type: int,
        inside_filled: int,
        anim_start: float,
        animate: bool,
    ):
        connector = self._connector if inside_filled else self._hybrid_connector
        func = self.tile_function_map[(connector, inside_filled)]

        base_tile = func(
            tile_type,
            self._edge_length,
            self._line_width,
            self._line_color,
            self._fill_color,
            self._bg_color,
            animate,
            anim_start,
            self._animation_duration,
        )

        return dw.Use(base_tile, x_offset, y_offset)

    def _draw_grid_lines(self):
        for i in range(self._dimension + 1):
            self._svg_top_group.append(
                dw.Line(
                    0,
                    i * self._edge_length,
                    self._draw_size,
                    i * self._edge_length,
                    stroke=self._grid_color,
                    stroke_width=self._grid_line_width,
                )
            )
            self._svg_top_group.append(
                dw.Line(
                    i * self._edge_length,
                    0,
                    i * self._edge_length,
                    self._draw_size,
                    stroke=self._grid_color,
                    stroke_width=self._grid_line_width,
                )
            )
