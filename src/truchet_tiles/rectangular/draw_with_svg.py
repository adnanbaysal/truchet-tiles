import math
import pathlib

from enum import Enum

import drawsvg as dw
import pygame
import pygame.gfxdraw

CURR_DIR = pathlib.Path(__file__).parent.resolve()

SVG_BLACK = "#000000"
SVG_WHITE = "#FFFFFF"

PYG_BLACK = (0, 0, 0)
PYG_WHITE = (255, 255, 255)


class FillStyle(str, Enum):
    linear = "linear"
    filled = "filled"


class CurveStyle(str, Enum):
    straight = "straight"
    curved = "curved"


class AxisAlignmentStyle(str, Enum):
    aligned = "aligned"
    rotated = "rotated"


class TilingColor(int, Enum):
    base = 0
    inverted = 1


class DrawTruchetSVG:
    MAX_LINE_WIDTH = 32
    DISPLAY_FILE_PATH = (CURR_DIR / "truchet.png").as_posix()

    def __init__(self, grid: list[list[int]], tile_size: int) -> None:
        self.grid = grid

        assert tile_size > 0, "tile_size must be positive"
        self._t_end = tile_size
        self._t_mid = int(self._t_end / 2)
        self._grid_size = len(self._grid)
        self._draw_size = self._grid_size * self._t_end

        self._fill_style = FillStyle.linear
        self._curve_style = CurveStyle.straight
        self._alignment_style = AxisAlignmentStyle.rotated

        self._tiling_color = TilingColor.base
        self._line_width = 1

        self._hybrid_fill = 0  # if > 0, mixes curved and straight fills

        self._screen = pygame.display.set_mode((self._draw_size, self._draw_size))
        self._screen.fill(PYG_WHITE)
        self._svg = dw.Drawing(
            self._draw_size, self._draw_size, id_prefix="truchet_tiling"
        )
        self._svg_top_group = dw.Group(
            id="truchet_group", fill="none"
        )  # To handle translations
        self._svg.save_png(self.DISPLAY_FILE_PATH)
        self._draw_surface = pygame.image.load(self.DISPLAY_FILE_PATH)

        self._base_tiles = {}
        self._create_base_tiles()

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, value):
        assert all(
            len(row) == len(value) for row in value
        ), "grid should have the same number of rows as the number of columns"
        self._grid = value

    # LEVEL 1 base tile function:
    def _create_base_tiles(self):
        self._base_tiles[FillStyle.linear] = {}
        self._base_tiles[FillStyle.filled] = {}

        self._create_linear_base_tiles()
        self._create_filled_base_tiles()

    # LEVEL 2 base tile functions
    def _create_linear_base_tiles(self):
        self._create_linear_straight_base_tiles()
        self._create_linear_curved_base_tiles()

    def _create_filled_base_tiles(self):
        self._create_filled_straight_base_tiles()
        self._create_filled_curved_base_tiles()

    # LEVEL 3 base tile functions
    def _create_linear_straight_base_tiles(self):
        self._base_tiles[FillStyle.linear][CurveStyle.straight] = []
        self._create_linear_straight_base_tile(0)
        self._create_linear_straight_base_tile(1)

    def _create_linear_curved_base_tiles(self):
        self._base_tiles[FillStyle.linear][CurveStyle.curved] = []
        self._create_linear_curved_base_tile(0)
        self._create_linear_curved_base_tile(1)

    def _create_filled_straight_base_tiles(self):
        self._base_tiles[FillStyle.filled][CurveStyle.straight] = []
        # Fill area out of diagonal lines
        self._create_outside_filled_straight_base_tile(0)
        self._create_outside_filled_straight_base_tile(1)

        # Fill area beween diagonal lines
        self._create_inside_filled_straight_base_tile(0)
        self._create_inside_filled_straight_base_tile(1)

    def _create_filled_curved_base_tiles(self):
        self._base_tiles[FillStyle.filled][CurveStyle.curved] = []
        # Fill area outside of arc lines
        self._create_outside_filled_curved_base_tile(0)
        self._create_outside_filled_curved_base_tile(1)

        # Fill area between arc lines
        self._create_inside_filled_curved_base_tile(0)
        self._create_inside_filled_curved_base_tile(1)

    # LEVEL 4 base tile functions
    def _create_linear_straight_base_tile(self, tile_type: int):
        left1 = (0, self._t_mid)
        right1 = (self._t_end, self._t_mid)

        if tile_type == 0:
            left2 = (self._t_mid, self._t_end)
            right2 = (self._t_mid, 0)
        else:
            left2 = (self._t_mid, 0)
            right2 = (self._t_mid, self._t_end)

        line_left = dw.Line(
            *left1, *left2, stroke_width=self._line_width, stroke=SVG_BLACK
        )
        line_right = dw.Line(
            *right1, *right2, stroke_width=self._line_width, stroke=SVG_BLACK
        )

        ls = dw.Group(id=f"ls{tile_type}", fill="none")
        ls.append(line_left)
        ls.append(line_right)

        self._base_tiles[FillStyle.linear][CurveStyle.straight].append(ls)

    def _create_linear_curved_base_tile(self, tile_type: int):
        if tile_type == 1:
            left_center = (0, 0)
            left_degrees = (90, 0)
            right_center = (self._t_end, self._t_end)
            right_degrees = (270, 180)
        else:
            left_center = (0, self._t_end)
            left_degrees = (360, 270)
            right_center = (self._t_end, 0)
            right_degrees = (180, 90)

        curve_left = dw.Arc(
            *left_center,
            self._t_mid,
            *left_degrees,
            stroke_width=self._line_width,
            stroke=SVG_BLACK,
        )

        curve_right = dw.Arc(
            *right_center,
            self._t_mid,
            *right_degrees,
            stroke_width=self._line_width,
            stroke=SVG_BLACK,
        )

        lc = dw.Group(id=f"lc{tile_type}", fill="none")
        lc.append(curve_left)
        lc.append(curve_right)

        self._base_tiles[FillStyle.linear][CurveStyle.curved].append(lc)

    def _create_outside_filled_straight_base_tile(self, tile_type: int):
        left0 = (0, self._t_mid)
        right0 = (self._t_end, self._t_mid)

        if tile_type == 0:
            left1 = (self._t_mid, self._t_end)
            left2 = (0, self._t_end)
            right1 = (self._t_mid, 0)
            right2 = (self._t_end, 0)
        else:
            left1 = (self._t_mid, 0)
            left2 = (0, 0)
            right1 = (self._t_mid, self._t_end)
            right2 = (self._t_end, self._t_end)

        triangle_left = dw.Lines(
            *left0,
            *left1,
            *left2,
            fill=SVG_BLACK,
            stroke=SVG_BLACK,
            close="true",
        )

        triangle_right = dw.Lines(
            *right0,
            *right1,
            *right2,
            fill=SVG_BLACK,
            stroke=SVG_BLACK,
            close="true",
        )

        fos = dw.Group(id=f"fos{tile_type}", fill="none")
        fos.append(triangle_left)
        fos.append(triangle_right)

        self._base_tiles[FillStyle.filled][CurveStyle.straight].append(fos)

    def _get_hexagon_points(self, tile_type: int):
        p0 = (0, self._t_mid)
        p3 = (self._t_end, self._t_mid)

        if tile_type == 0:
            p1 = (self._t_mid, self._t_end)
            p2 = (self._t_end, self._t_end)
            p4 = (self._t_mid, 0)
            p5 = (0, 0)
        else:
            p1 = (0, self._t_end)
            p2 = (self._t_mid, self._t_end)
            p4 = (self._t_end, 0)
            p5 = (self._t_mid, 0)

        return (*p0, *p1, *p2, *p3, *p4, *p5)

    def _create_inside_filled_straight_base_tile(self, tile_type: int):
        hexagon_points = self._get_hexagon_points(tile_type)

        hexagon = dw.Lines(
            *hexagon_points,
            fill=SVG_BLACK,
            stroke=SVG_BLACK,
            close="true",
        )

        fis = dw.Group(id=f"fis{tile_type}", fill="none")
        fis.append(hexagon)

        self._base_tiles[FillStyle.filled][CurveStyle.straight].append(fis)

    def _create_outside_filled_curved_base_tile(self, tile_type: int):
        if tile_type == 1:
            left_center = (0, 0)
            right_center = (self._t_end, self._t_end)
        else:
            left_center = (0, self._t_end)
            right_center = (self._t_end, 0)

        pie_lef = self._create_circle_pie(left_center)
        pie_right = self._create_circle_pie(right_center)
        hexagon_points = self._get_hexagon_points(tile_type)
        white_hexagon = dw.Lines(
            *hexagon_points,
            stroke=SVG_WHITE,
            fill=SVG_WHITE,
            closed=True,
        )

        foc = dw.Group(id=f"foc{tile_type}", fill="none")
        foc.append(white_hexagon)
        foc.append(pie_lef)
        foc.append(pie_right)

        self._base_tiles[FillStyle.filled][CurveStyle.curved].append(foc)

    def _create_inside_filled_curved_base_tile(self, tile_type: int):
        if tile_type == 1:
            la_center = (0, 0)
            ra_center = (self._t_end, self._t_end)
        else:
            la_center = (0, self._t_end)
            ra_center = (self._t_end, 0)

        pie_left = self._create_circle_pie(la_center, color=SVG_WHITE)
        pie_right = self._create_circle_pie(ra_center, color=SVG_WHITE)

        hexagon_points = self._get_hexagon_points(tile_type)
        black_hexagon = dw.Lines(
            *hexagon_points,
            stroke=SVG_BLACK,
            fill=SVG_BLACK,
            closed=True,
        )

        fic = dw.Group(id=f"fic{tile_type}", fill="none")
        fic.append(black_hexagon)
        fic.append(pie_left)
        fic.append(pie_right)

        self._base_tiles[FillStyle.filled][CurveStyle.curved].append(fic)

    def _create_circle_pie(self, center, color=SVG_BLACK):
        pie = dw.Circle(
            *center,
            self._t_mid,
            fill=color,
            path_length=math.pi * self._t_mid / 2,
        )
        return pie

    def draw(self):
        if self._fill_style == FillStyle.linear:
            self._draw_linear()
        else:
            self._draw_filled()

    def _draw_linear(self):
        self._clear_screan()

        for grid_row in range(self._grid_size):
            y_offset = grid_row * self._t_end
            for grid_col in range(self._grid_size):
                x_offset = grid_col * self._t_end

                if self._curve_style == CurveStyle.straight:
                    self._draw_tile_linear_straight(
                        x_offset, y_offset, self._grid[grid_row][grid_col]
                    )
                else:
                    self._draw_tile_linear_curved(
                        x_offset, y_offset, self._grid[grid_row][grid_col]
                    )

        self._show_screen()

    def _clear_screan(self):
        self._svg.clear()
        self._svg = dw.Drawing(
            self._draw_size, self._draw_size, id_prefix="truchet_tiling"
        )
        self._svg_top_group = dw.Group(id="truchet_group", fill="none")
        self._screen.fill(PYG_WHITE)

    def _get_transform(self):
        return (
            f"matrix(.5 -.5 .5 .5 0 {self._t_end * self._grid_size / 2})"
            if self._alignment_style == AxisAlignmentStyle.aligned
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

    def _draw_tile_linear_straight(self, x_offset: int, y_offset: int, cell_value: int):
        self._svg_top_group.append(
            dw.Use(
                self._base_tiles[FillStyle.linear][CurveStyle.straight][cell_value],
                x_offset,
                y_offset,
            )
        )

    def _draw_tile_linear_curved(self, x_offset: int, y_offset: int, cell_value: int):
        self._svg_top_group.append(
            dw.Use(
                self._base_tiles[FillStyle.linear][CurveStyle.curved][cell_value],
                x_offset,
                y_offset,
            )
        )

    def _draw_filled(self):
        self._clear_screan()
        grid_of_fill_side = self._generate_fill_inside_grid()

        for grid_row in range(self._grid_size):
            y_offset = grid_row * self._t_end
            for grid_col in range(self._grid_size):
                x_offset = grid_col * self._t_end

                svg_tile_index = (
                    self._grid[grid_row][grid_col]
                    + 2 * grid_of_fill_side[grid_row][grid_col]
                )

                if self._curve_style == CurveStyle.straight:
                    self._draw_tile_filled_straight(x_offset, y_offset, svg_tile_index)
                else:
                    self._draw_tile_filled_curved(x_offset, y_offset, svg_tile_index)

        self._show_screen()

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

    def _draw_tile_filled_straight(self, x_offset: int, y_offset: int, tile_index: int):
        self._svg_top_group.append(
            dw.Use(
                self._base_tiles[FillStyle.filled][CurveStyle.straight][tile_index],
                x_offset,
                y_offset,
            )
        )

    def _draw_tile_filled_curved(self, x_offset: int, y_offset: int, tile_index: int):
        outside = tile_index < 2
        inside = tile_index > 1
        h_not_2 = self._hybrid_fill in (0, 1)
        h_not_1 = self._hybrid_fill in (0, 2)
        inverted = self._tiling_color == TilingColor.base

        if (
            (inside and h_not_2 and inverted)
            or (outside and h_not_1 and inverted)
            or (inside and h_not_1 and not inverted)
            or (outside and h_not_2 and not inverted)
        ):
            self._svg_top_group.append(
                dw.Use(
                    self._base_tiles[FillStyle.filled][CurveStyle.curved][tile_index],
                    x_offset,
                    y_offset,
                )
            )
        else:
            self._svg_top_group.append(
                dw.Use(
                    self._base_tiles[FillStyle.filled][CurveStyle.straight][tile_index],
                    x_offset,
                    y_offset,
                )
            )

    def next_hybrid_mode(self):
        self._hybrid_fill = (self._hybrid_fill + 1) % 3

    def invert_color(self):
        self._tiling_color = (
            TilingColor.base
            if self._tiling_color == TilingColor.inverted
            else TilingColor.inverted
        )

    def increase_line_width(self):
        self._line_width = (
            self._line_width + 1 if self._line_width != self.MAX_LINE_WIDTH else 1
        )
        self._create_linear_base_tiles()

    def decrease_line_width(self):
        self._line_width = (
            self._line_width - 1 if self._line_width != 1 else self.MAX_LINE_WIDTH
        )
        self._create_linear_base_tiles()

    def invert_aligned(self):
        self._alignment_style = (
            AxisAlignmentStyle.aligned
            if self._alignment_style == AxisAlignmentStyle.rotated
            else AxisAlignmentStyle.rotated
        )

    def invert_curved(self):
        self._curve_style = (
            CurveStyle.curved
            if self._curve_style == CurveStyle.straight
            else CurveStyle.straight
        )

    def invert_filled(self):
        self._fill_style = (
            FillStyle.filled
            if self._fill_style == FillStyle.linear
            else FillStyle.linear
        )

    def tiling_identifier(self) -> str:
        return (
            f"{self._grid_size}x{self._t_end}px_"
            f"{'filled' if self._fill_style == FillStyle.filled else 'line'}_"
            f"{'curved' if self._curve_style == CurveStyle.curved else 'straight'}_"
            f"{'aligned' if self._alignment_style == AxisAlignmentStyle.aligned else 'rotated'}_"
            f"w{self._line_width}"
            f"{'hybrid' + str(self._hybrid_fill) + '_' if self._hybrid_fill > 0 else ''}"
        )

    def save_svg(self, filepath: str | pathlib.Path):
        self._svg.save_svg(filepath)
