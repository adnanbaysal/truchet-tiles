import drawsvg as dw  # type: ignore

from truchet_tiles.common.enum import (
    SvgColors,
    Connector,
    Filledness,
    HybridFill,
)
from truchet_tiles.rectangular.draw.enum import (
    RectAnimationMethod,
    AxisAlignment,
)
from truchet_tiles.rectangular.draw.tile_generator import RectTileGenerator


class RectTilingDrawer:
    ANIMATION_DELAY = "0.000001s"
    ANIMATION_BEGIN = 1.0

    def __init__(
        self,
        grid: list[list[int]],
        edge_length: int,
        align_to_axis: bool = False,
        fill: bool = False,
        connector: str = "straight",
        hybrid_mode: int = 0,
        animate: bool = False,
        animation_duration: float = 1.0,
        animation_method: str = "at_once",
        show_grid: bool = False,
        line_width: int = 1,
        max_line_width: int = 32,
        grid_line_width: float = 0.5,
        line_color: str = SvgColors.BLACK,
        bg_color: str = SvgColors.WHITE,
        fill_color: str = SvgColors.BLACK,
        grid_color: str = SvgColors.RED,
    ) -> None:
        assert all(
            len(row) == len(grid) for row in grid
        ), "grid should have the same number of rows as the number of columns"
        self._grid = grid

        assert edge_length > 0, "eldge_length must be positive"
        self._t_end = edge_length
        self._t_mid = int(self._t_end / 2)
        self._grid_size = len(self._grid)
        self._draw_size = self._grid_size * self._t_end

        self._max_line_width = max_line_width
        self._line_width = line_width

        self._fill_style = Filledness.filled if fill else Filledness.linear
        self._connector = Connector(connector)
        self._alignment_style = (
            AxisAlignment.aligned if align_to_axis else AxisAlignment.rotated
        )
        self._hybrid_fill = HybridFill(hybrid_mode)

        self._show_grid_lines = show_grid
        self._grid_line_width = grid_line_width
        self._grid_color = grid_color

        self._line_color = line_color
        self._bg_color = bg_color
        self._fill_color = fill_color

        self._animate = animate
        self._animation_method = RectAnimationMethod(animation_method)
        self._animation_prev_grid = [[0] * self._grid_size] * self._grid_size
        self._animation_rotation_dur = animation_duration

        self._svg = dw.Drawing(
            self._draw_size, self._draw_size, id_prefix="rect_truchet_tiling"
        )
        self._svg_top_group = dw.Group(
            id="truchet_group", fill="none"
        )  # To handle translations

        self._base_tiles = RectTileGenerator(
            edge_length,
            max_line_width=self._max_line_width,
            line_color=self._line_color,
            fill_color=self._fill_color,
            bg_color=self._bg_color,
        )

    @property
    def svg(self):
        return self._svg

    def draw(self):
        # TODO: Fix svg to png issue on windows
        self._clear_screan()

        if self._fill_style == Filledness.linear:
            self._draw_linear()
        else:
            self._draw_filled()

        if self._show_grid_lines:
            self._draw_grid_lines()

        self._update_svg()

    def _draw_linear(self):
        anim_start = self.ANIMATION_BEGIN
        for row in range(self._grid_size):
            for col in range(self._grid_size):
                self._insert_linear_tile(row, col, anim_start)

                if self._animation_method == RectAnimationMethod.by_tile:
                    if self._grid[row][col] != self._animation_prev_grid[row][col]:
                        anim_start += self._animation_rotation_dur

            if self._animation_method == RectAnimationMethod.by_row:
                anim_start += self._animation_rotation_dur

    def _clear_screan(self):
        self._svg.clear()
        self._svg = dw.Drawing(
            self._draw_size, self._draw_size, id_prefix="truchet_tiling"
        )
        self._svg_top_group = dw.Group(id="truchet_group", fill="none")

    def _get_transform(self):
        return (
            f"matrix(.5 -.5 .5 .5 0 {self._t_end * self._grid_size / 2})"
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

    def _insert_linear_tile(self, row: int, col: int, anim_start: float):
        y_offset = row * self._t_end
        x_offset = col * self._t_end

        used_tile = dw.Use(
            self._base_tiles[Filledness.linear][self._connector][self._line_width][
                self._grid[row][col]
            ],
            x_offset,
            y_offset,
        )
        if self._animate and (
            self._animation_prev_grid[row][col] != self._grid[row][col]
        ):

            def _get_rotation(begin, dur, start_deg, end_deg):
                return dw.AnimateTransform(
                    attributeName="transform",
                    begin=begin,
                    dur=dur,
                    type="rotate",
                    from_or_values=f"{start_deg} {x_offset + self._t_mid} {y_offset + self._t_mid}",
                    to=f"{end_deg} {x_offset + self._t_mid} {y_offset + self._t_mid}",
                    fill="freeze",
                    repeatCount="1",
                )

            # The following animation will make the svg appear to start from the prev state
            used_tile.append_anim(
                _get_rotation(self.ANIMATION_DELAY, self.ANIMATION_DELAY, 0, 90)
            )
            used_tile.append_anim(
                _get_rotation(anim_start, self._animation_rotation_dur, 90, 180)
            )

        self._svg_top_group.append(used_tile)

    def _draw_filled(self):
        grid_of_fill_side = self._generate_fill_inside_grid()

        for grid_row in range(self._grid_size):
            y_offset = grid_row * self._t_end
            for grid_col in range(self._grid_size):
                x_offset = grid_col * self._t_end

                base_tile_index = (
                    self._grid[grid_row][grid_col]
                    + 2 * grid_of_fill_side[grid_row][grid_col]
                )

                if self._connector == Connector.straight:
                    self._insert_filled_straight_tile(
                        x_offset, y_offset, base_tile_index
                    )
                elif self._connector == Connector.curved:
                    self._insert_filled_curved_tile(x_offset, y_offset, base_tile_index)
                else:
                    self._insert_filled_twoline_tile(
                        x_offset, y_offset, base_tile_index
                    )

    def _generate_fill_inside_grid(self) -> list[list[int]]:
        _grid: list[list[int]] = []
        for grid_row in range(self._grid_size):
            _grid.append([])
            for grid_col in range(self._grid_size):
                neighbor = self._neighbor_cell(self._grid, grid_row, grid_col)
                bit_changed = self._grid[grid_row][grid_col] ^ neighbor
                if grid_row == 0 and grid_col == 0:
                    neighbor_fill = self._grid[0][0]
                else:
                    neighbor_fill = self._neighbor_cell(_grid, grid_row, grid_col)
                _grid[grid_row].append(neighbor_fill ^ bit_changed ^ 1)

        return _grid

    @staticmethod
    def _neighbor_cell(_grid: list[list[int]], row: int, col: int) -> int:
        if row == 0 and col == 0:
            return _grid[row][col]
        if col > 0:
            return _grid[row][col - 1]
        if row > 0:
            return _grid[row - 1][col]
        raise ValueError("Invalid row and column")

    def _insert_filled_straight_tile(
        self, x_offset: int, y_offset: int, tile_index: int
    ):
        self._svg_top_group.append(
            dw.Use(
                self._base_tiles[Filledness.filled][Connector.straight][
                    self._line_width
                ][tile_index],
                x_offset,
                y_offset,
            )
        )

    def _insert_filled_curved_tile(self, x_offset: int, y_offset: int, tile_index: int):
        outside = tile_index < 2
        inside = tile_index > 1
        h_not_2 = self._hybrid_fill in (HybridFill.none, HybridFill.hybrid_1)
        h_not_1 = self._hybrid_fill in (HybridFill.none, HybridFill.hybrid_2)

        if (inside and h_not_2) or (outside and h_not_1):
            self._svg_top_group.append(
                dw.Use(
                    self._base_tiles[Filledness.filled][Connector.curved][
                        self._line_width
                    ][tile_index],
                    x_offset,
                    y_offset,
                )
            )
        else:
            self._svg_top_group.append(
                dw.Use(
                    self._base_tiles[Filledness.filled][Connector.straight][
                        self._line_width
                    ][tile_index],
                    x_offset,
                    y_offset,
                )
            )

    def _insert_filled_twoline_tile(
        self, x_offset: int, y_offset: int, tile_index: int
    ):
        self._svg_top_group.append(
            dw.Use(
                self._base_tiles[Filledness.filled][Connector.twoline][
                    self._line_width
                ][tile_index],
                x_offset,
                y_offset,
            )
        )

    def _draw_grid_lines(self):
        for i in range(self._grid_size + 1):
            self._svg_top_group.append(
                dw.Line(
                    0,
                    i * self._t_end,
                    self._draw_size,
                    i * self._t_end,
                    stroke=self._grid_color,
                    stroke_width=self._grid_line_width,
                )
            )
            self._svg_top_group.append(
                dw.Line(
                    i * self._t_end,
                    0,
                    i * self._t_end,
                    self._draw_size,
                    stroke=self._grid_color,
                    stroke_width=self._grid_line_width,
                )
            )
