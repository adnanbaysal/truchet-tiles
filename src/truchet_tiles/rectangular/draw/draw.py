import pathlib

import drawsvg as dw
import pygame
import pygame.gfxdraw

from .enum import Colors, AxisAlignment, Curvedness, Filledness, HybridFill, TilingColor
from .tile_generator import TileGenerator


CURR_DIR = pathlib.Path(__file__).parent.resolve()


class TilingDrawer:
    DISPLAY_FILE_PATH = (CURR_DIR / "truchet.png").as_posix()

    def __init__(
        self, grid: list[list[int]], tile_size: int, max_line_width: int = 32
    ) -> None:
        assert all(
            len(row) == len(grid) for row in grid
        ), "grid should have the same number of rows as the number of columns"
        self._grid = grid

        assert tile_size > 0, "tile_size must be positive"
        self._t_end = tile_size
        self._t_mid = int(self._t_end / 2)
        self._grid_size = len(self._grid)
        self._draw_size = self._grid_size * self._t_end

        self._max_line_width = max_line_width
        self._line_width = 1

        self._fill_style = Filledness.linear
        self._curve_style = Curvedness.straight
        self._alignment_style = AxisAlignment.rotated
        self._tiling_color = TilingColor.base
        self._hybrid_fill = HybridFill.none

        self._show_grid_lines = False

        self._screen = pygame.display.set_mode((self._draw_size, self._draw_size))
        self._screen.fill(Colors.PYG_WHITE)
        self._svg = dw.Drawing(
            self._draw_size, self._draw_size, id_prefix="truchet_tiling"
        )
        self._svg_top_group = dw.Group(
            id="truchet_group", fill="none"
        )  # To handle translations
        self._svg.save_png(self.DISPLAY_FILE_PATH)
        self._draw_surface = pygame.image.load(self.DISPLAY_FILE_PATH)

        self._base_tiles = TileGenerator(tile_size, max_line_width=self._max_line_width)

    def draw(self):
        # TODO: Fix svg to png issue on windows
        self._clear_screan()

        if self._fill_style == Filledness.linear:
            self._draw_linear()
        else:
            self._draw_filled()

        if self._show_grid_lines:
            self._draw_grid_lines()

        self._show_screen()

    def update_grid(self, grid: list[list[int]]):
        assert all(
            len(row) == len(grid) for row in grid
        ), "grid should have the same number of rows as the number of columns"
        self._grid = grid
        self.draw()

    def next_hybrid_mode(self):
        hybrid_before = self._hybrid_fill
        hybrid_after = (hybrid_before + 1) % 3
        self._hybrid_fill = HybridFill(hybrid_after)
        self.draw()

    def invert_color(self):
        self._tiling_color = (
            TilingColor.base
            if self._tiling_color == TilingColor.inverted
            else TilingColor.inverted
        )
        self.draw()

    def increase_line_width(self):
        self._line_width = (
            self._line_width + 1 if self._line_width != self._max_line_width else 1
        )
        self.draw()

    def decrease_line_width(self):
        self._line_width = (
            self._line_width - 1 if self._line_width != 1 else self._max_line_width
        )
        self.draw()

    def invert_aligned(self):
        self._alignment_style = (
            AxisAlignment.aligned
            if self._alignment_style == AxisAlignment.rotated
            else AxisAlignment.rotated
        )
        self.draw()

    def invert_curved(self):
        self._curve_style = (
            Curvedness.curved
            if self._curve_style == Curvedness.straight
            else Curvedness.straight
        )
        self.draw()

    def invert_filled(self):
        self._fill_style = (
            Filledness.filled
            if self._fill_style == Filledness.linear
            else Filledness.linear
        )
        self.draw()

    def invert_show_grid_lines(self):
        self._show_grid_lines = self._show_grid_lines ^ True
        self.draw()

    def tiling_identifier(self) -> str:
        return (
            f"{self._grid_size}x{self._t_end}px_"
            f"{'filled' if self._fill_style == Filledness.filled else 'line'}_"
            f"{'curved' if self._curve_style == Curvedness.curved else 'straight'}_"
            f"{'aligned' if self._alignment_style == AxisAlignment.aligned else 'rotated'}_"
            f"w{self._line_width}"
            f"{'hybrid' + str(self._hybrid_fill.value) + '_' if self._hybrid_fill.value > 0 else ''}"
        )

    def save_svg(self, filepath: str | pathlib.Path):
        self._svg.save_svg(filepath)

    def _draw_linear(self):
        for grid_row in range(self._grid_size):
            y_offset = grid_row * self._t_end
            for grid_col in range(self._grid_size):
                x_offset = grid_col * self._t_end
                self._insert_linear_tile(
                    x_offset,
                    y_offset,
                    self._curve_style,
                    self._grid[grid_row][grid_col],
                )

    def _clear_screan(self):
        self._svg.clear()
        self._svg = dw.Drawing(
            self._draw_size, self._draw_size, id_prefix="truchet_tiling"
        )
        self._svg_top_group = dw.Group(id="truchet_group", fill="none")
        self._screen.fill(Colors.PYG_WHITE)

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

    def _show_screen(self):
        self._update_svg()
        self._svg.save_png(self.DISPLAY_FILE_PATH)
        self._draw_surface = pygame.image.load(self.DISPLAY_FILE_PATH)
        self._screen.blit(self._draw_surface, (0, 0))

    def _insert_linear_tile(
        self, x_offset: int, y_offset: int, curvedness: Curvedness, cell_value: int
    ):
        self._svg_top_group.append(
            dw.Use(
                self._base_tiles[Filledness.linear][curvedness][self._line_width][
                    cell_value
                ],
                x_offset,
                y_offset,
            )
        )

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

                if self._curve_style == Curvedness.straight:
                    self._insert_filled_straight_tile(
                        x_offset, y_offset, base_tile_index
                    )
                else:
                    self._insert_filled_curved_tile(x_offset, y_offset, base_tile_index)

    def _generate_fill_inside_grid(self) -> list[list[int]]:
        _grid: list[list[int]] = []
        for grid_row in range(self._grid_size):
            _grid.append([])
            for grid_col in range(self._grid_size):
                neighbor = self._neighbor_cell(self._grid, grid_row, grid_col)
                bit_changed = self._grid[grid_row][grid_col] ^ neighbor
                if grid_row == 0 and grid_col == 0:
                    neighbor_fill = self._grid[0][0] ^ self._tiling_color.value
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
                self._base_tiles[Filledness.filled][Curvedness.straight][tile_index],
                x_offset,
                y_offset,
            )
        )

    def _insert_filled_curved_tile(self, x_offset: int, y_offset: int, tile_index: int):
        outside = tile_index < 2
        inside = tile_index > 1
        h_not_2 = self._hybrid_fill in (HybridFill.none, HybridFill.hybrid_1)
        h_not_1 = self._hybrid_fill in (HybridFill.none, HybridFill.hybrid_2)
        inverted = self._tiling_color == TilingColor.base

        if (
            (inside and h_not_2 and inverted)
            or (outside and h_not_1 and inverted)
            or (inside and h_not_1 and not inverted)
            or (outside and h_not_2 and not inverted)
        ):
            self._svg_top_group.append(
                dw.Use(
                    self._base_tiles[Filledness.filled][Curvedness.curved][tile_index],
                    x_offset,
                    y_offset,
                )
            )
        else:
            self._svg_top_group.append(
                dw.Use(
                    self._base_tiles[Filledness.filled][Curvedness.straight][
                        tile_index
                    ],
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
                    stroke=Colors.SVG_RED,
                )
            )
            self._svg_top_group.append(
                dw.Line(
                    i * self._t_end,
                    0,
                    i * self._t_end,
                    self._draw_size,
                    stroke=Colors.SVG_RED,
                )
            )
