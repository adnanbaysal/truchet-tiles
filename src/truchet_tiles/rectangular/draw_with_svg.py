import pathlib

from enum import Enum

import drawsvg as dw
import pygame
import pygame.gfxdraw

CURR_DIR = pathlib.Path(__file__).parent.resolve()


class FillStyle(str, Enum):
    linear = "linear"
    filled = "filled"


class CurveStyle(str, Enum):
    straight = "straight"
    curved = "curved"


class AxisAlignmentStyle(str, Enum):
    aligned = "aligned"
    rotated = "rotated"


class DrawTruchetSVG:
    MAX_LINE_WIDTH = 64
    PNG_FILE_PATH = (CURR_DIR / "truchet.png").as_posix()

    def __init__(self, grid: list[list[int]], tile_size: int) -> None:
        self.grid = grid

        assert tile_size > 0, "tile_size must be positive"
        self._tile_size = tile_size
        self._tile_mid = int(self._tile_size / 2)
        self._grid_size = len(self._grid)
        self._draw_size = self._grid_size * self._tile_size    
        
        self._fill_style = FillStyle.linear
        self._curve_style = CurveStyle.straight
        self._alignment_style = AxisAlignmentStyle.rotated

        self._color = 0
        self._fill_color = (0, 0, 0)
        self._draw_background = (255, 255, 255)
        self._line_color = "#000000"
        self._line_width = 1

        self._hybrid_fill = 0  # if > 0, mixes curved and straight fills

        self._screen = pygame.display.set_mode((self._draw_size, self._draw_size))
        self._screen.fill(self._draw_background)
        self._svg = dw.Drawing(self._draw_size, self._draw_size, id_prefix='pic')
        self._svg_top_group = dw.Group(id="truchet_group", fill="none")  # To handle translations
        self._svg.save_png(self.PNG_FILE_PATH)
        self._draw_surface = pygame.image.load(self.PNG_FILE_PATH)

        self._base_tiles = {
            FillStyle.linear: {
                CurveStyle.straight: [],
                CurveStyle.curved: [],
            },
            FillStyle.filled: {
                CurveStyle.straight: [],
                CurveStyle.curved: [],
            },
        }
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
        self._create_linear_base_tiles()
        # self._create_filled_base_tiles()  # Uncomment after implementation

    # LEVEL 2 base tile functions
    def _create_linear_base_tiles(self):
        self._create_linear_straight_base_tiles()
        # self._create_linear_curved_base_tiles()  # Uncomment after implementation

    def _create_filled_base_tiles(self):
        self._create_filled_straight_base_tiles()
        self._create_filled_curved_base_tiles()
        
    # LEVEL 3 base tile functions
    def _create_linear_straight_base_tiles(self):
        self._create_linear_straight_base_tile(0)
        self._create_linear_straight_base_tile(1)

    def _create_linear_curved_base_tiles(self):
        self._create_linear_curved_base_tile(0)
        self._create_linear_curved_base_tile(1)

    def _create_filled_straight_base_tiles(self):
        # Fill area beween diagonal lines
        self._create_filled_straight_base_tile(0)
        self._create_filled_straight_base_tile(1)

        # Fill area out of diagonal lines
        self._create_filled_straight_base_tile(2)
        self._create_filled_straight_base_tile(3)

    def _create_filled_curved_base_tiles(self):
        # Fill area betweendiagonal lines
        self._create_filled_curved_base_tile(0)
        self._create_filled_curved_base_tile(1)

        # Fill area outside of diagonal lines
        self._create_filled_curved_base_tile(2)
        self._create_filled_curved_base_tile(3)

    # LEVEL 4 base tile functions
    def _create_linear_straight_base_tile(self, tile_type: int):
        left1 = (0, self._tile_mid)
        right1 = (self._tile_size, self._tile_mid)

        if tile_type == 0:
            left2 = (self._tile_mid, self._tile_size)
            right2 = (self._tile_mid, 0)
        else:
            left2 = (self._tile_mid, 0)
            right2 = (self._tile_mid, self._tile_size)

        line_left = dw.Line(*left1, *left2, stroke_width=self._line_width, stroke=self._line_color)
        line_right = dw.Line(*right1, *right2, stroke_width=self._line_width, stroke=self._line_color)
        
        sl = dw.Group(id=f"sl{tile_type}", fill="none")
        sl.append(line_left)
        sl.append(line_right)

        self._base_tiles[FillStyle.linear][CurveStyle.straight].append(sl)

    def _create_linear_curved_base_tile(self, tile_type: int):
        raise NotImplementedError()

    def _create_filled_straight_base_tile(self, tile_type: int):
        raise NotImplementedError()

    def _create_filled_curved_base_tile(self, tile_type: int):
        raise NotImplementedError()

    def draw(self):
        if self._fill_style == FillStyle.linear:
            self._draw_linear()
        else:
            self._draw_filled()

    def _draw_linear(self):
        self._clear_screan()
        
        for grid_row in range(self._grid_size):
            y_offset = grid_row * self._tile_size
            for grid_col in range(self._grid_size):
                x_offset = grid_col * self._tile_size

                if self._curve_style == CurveStyle.straight:
                    self._draw_tile_linear_straight(x_offset, y_offset, self._grid[grid_row][grid_col])
                else:
                    self._draw_tile_linear_curved(x_offset, y_offset, self._grid[grid_row][grid_col])
        
        self._show_screen()

    def _clear_screan(self):
        self._svg.clear()
        self._svg_top_group = dw.Group(id="truchet_group", fill="none")
        self._screen.fill(self._draw_background)
        
    def _show_screen(self):
        self._svg.append(dw.Use(self._svg_top_group, 0, 0))
        self._svg.save_png(self.PNG_FILE_PATH)
        self._draw_surface = pygame.image.load(self.PNG_FILE_PATH)
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
        kwargs_left = {}
        kwargs_right = {}

        if cell_value == 1:
            center_left = (x_offset, y_offset)
            kwargs_left["draw_bottom_right"] = True
            center_right = (x_offset + self._tile_size, y_offset + self._tile_size)
            kwargs_right["draw_top_left"] = True
        else:
            center_left = (x_offset, y_offset + self._tile_size)
            kwargs_left["draw_top_right"] = True
            center_right = (x_offset + self._tile_size, y_offset)
            kwargs_right["draw_bottom_left"] = True
        
        pygame.draw.circle(
            self._draw_surface, self._line_color, center_left, self._tile_mid, width=self._line_width, **kwargs_left
        )
        pygame.draw.circle(
            self._draw_surface, self._line_color, center_right, self._tile_mid, width=self._line_width, **kwargs_right
        )

    def _fill_outside_straight(self, rotate: int, x: int, y: int, middle: int, end: int):
        # draw two triangles
        if not rotate:
            # left mid to top mid + bottom mid to right mid
            triangle1 = ((x, y), (x + middle, y), (x, y + middle))
            triangle2 = ((x + end, y + end), (x + middle, y + end), (x + end, y + middle))

        else:
            triangle1 = ((x + end, y), (x + end, y + middle), (x + middle, y))
            triangle2 = ((x, y + end), (x, y + middle), (x + middle, y + end))

        pygame.draw.polygon(self._draw_surface, self._fill_color, triangle1, width=0)
        pygame.draw.polygon(self._draw_surface, self._fill_color, triangle2, width=0)

    def _fill_inside_straight(self, rotate: int, x: int, y: int, middle: int, end: int):
        # draw hexagon
        if not rotate:
            points = (
                (x, y + end),
                (x, y + middle),
                (x + middle, y),
                (x + end, y),
                (x + end, y + middle),
                (x + middle, y + end),
            )
        else:
            points = (
                (x, y),
                (x + middle, y),
                (x + end, y + middle),
                (x + end, y + end),
                (x + middle, y + end),
                (x, y + middle),
            )

        pygame.draw.polygon(self._draw_surface, self._fill_color, points, width=0)

    def _draw_filled_tile_straight(self, fill_inside: int, rotate: int, x: int, y: int, middle: int, end: int):
        if fill_inside:
            self._fill_inside_straight(rotate, x, y, middle, end)
        else:
            self._fill_outside_straight(rotate, x, y, middle, end)

    def _get_arc_parameters(
        self, rotate: int, x: int, y: int, end: int
    ) -> tuple[tuple[int, int], dict[str, bool], tuple[int, int], dict[str, bool]]:
        if not rotate:
            # left mid to top mid + bottom mid to right mid
            center_left = (x, y)
            kwargs_left = {"draw_bottom_right": True}
            center_right = (x + end, y + end)
            kwargs_right = {"draw_top_left": True}
        else:
            center_left = (x, y + end)
            kwargs_left = {"draw_top_right": True}
            center_right = (x + end, y)
            kwargs_right = {"draw_bottom_left": True}

        return center_left, kwargs_left, center_right, kwargs_right

    def _fill_outside_curved(self, rotate: int, x: int, y: int, end: int):
        # quarter circles are black, bg is white
        center_left, kwargs_left, center_right, kwargs_right = self._get_arc_parameters(
            rotate, x, y, end
        )

        pygame.draw.circle(
            self._draw_surface, self._line_color, center_left, self._tile_mid, width=0, **kwargs_left
        )
        pygame.draw.circle(
            self._draw_surface, self._line_color, center_right, self._tile_mid, width=0, **kwargs_right
        )

    def _fill_inside_curved(self, rotate: int, x: int, y: int, end: int):
        # bg is black, quarter circles are white
        # draw a black square
        points = (
            (x, y),
            (x + end , y),
            (x + end, y + end),
            (x, y + end),
            (x , y),
        )
        pygame.draw.polygon(self._draw_surface, self._fill_color, points, width=0)

        # draw two white quarter circles
        center_left, kwargs_left, center_right, kwargs_right = self._get_arc_parameters(
            rotate, x, y, end
        )
        pygame.draw.circle(
            self._draw_surface, self._draw_background, center_left, self._tile_mid, width=0, **kwargs_left
        )
        pygame.draw.circle(
            self._draw_surface, self._draw_background, center_right, self._tile_mid, width=0, **kwargs_right
        )

    def _draw_filled_tile_curved(self, fill_inside: int, rotate: int, x: int, y: int, middle: int, end: int):
        if fill_inside:
            if self._hybrid_fill in (0, 1):
                self._fill_inside_curved(rotate, x, y, end)
            else:
                self._fill_inside_straight(rotate, x, y, middle, end)
        else:
            if self._hybrid_fill in (0, 2):
                self._fill_outside_curved(rotate, x, y, end)
            else:
                self._fill_outside_straight(rotate, x, y, middle, end)

    def _draw_filled_tile(
        self,
        fill_inside: int,
        rotate: int,
        x: int,
        y: int,
    ):
        middle = self._tile_mid
        end = self._tile_size

        if self._curve_style == CurveStyle.curved:
            self._draw_filled_tile_curved(fill_inside, rotate, x, y, middle, end)
        else:
            self._draw_filled_tile_straight(fill_inside, rotate, x, y, middle, end)

    @staticmethod
    def _neighbor_cell(_grid: list[list[int]], row: int, col: int) -> int:
        if row == 0 and col == 0:
            return _grid[row][col]
        if col > 0:
            return _grid[row][col - 1]
        if row > 0:
            return _grid[row - 1][col]
        raise ValueError("Invalid row and column")

    def _generate_fill_inside_grid(self) -> list[list[int]]:
        _grid: list[list[int]] = []
        for grid_row in range(self._grid_size):
            _grid.append([])
            for grid_col in range(self._grid_size):
                neighbor = self._neighbor_cell(self._grid, grid_row, grid_col)
                bit_changed = self._grid[grid_row][grid_col] ^ neighbor
                if grid_row == 0 and grid_col == 0:
                    neighbor_fill = self._grid[0][0] ^ self._color
                else:
                    neighbor_fill = self._neighbor_cell(_grid, grid_row, grid_col)
                _grid[grid_row].append(neighbor_fill ^ bit_changed ^ 1)

        return _grid

    def _draw_filled(self):
        self._clear_screan()
        grid_of_fill_inside = self._generate_fill_inside_grid()

        for grid_row in range(self._grid_size):
            y_offset = grid_row * self._tile_size
            for grid_col in range(self._grid_size):
                x_offset = grid_col * self._tile_size

                self._draw_filled_tile(
                    grid_of_fill_inside[grid_row][grid_col],
                    self._grid[grid_row][grid_col],
                    x_offset,
                    y_offset,
                )

        self._show_screen()

    def next_hybrid_mode(self):
        self._hybrid_fill = (self._hybrid_fill + 1) % 3

    def invert_color(self):
        self._color = self._color ^ 1

    def increase_line_width(self):
        self._line_width = self._line_width + 1 if self._line_width != self.MAX_LINE_WIDTH else 1

    def decrease_line_width(self):
        self._line_width = self._line_width - 1 if self._line_width != 1 else self.MAX_LINE_WIDTH

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
            f"{self._grid_size}x{self._tile_size}px_"
            f"{'filled' if self._fill_style == FillStyle.filled else 'line'}_"
            f"{'curved' if self._curve_style == CurveStyle.curved else 'straight'}_"
            f"{'aligned' if self._alignment_style == AxisAlignmentStyle.aligned else 'rotated'}_"
            f"w{self._line_width}"
            f"{'hybrid' + str(self._hybrid_fill) + '_' if self._hybrid_fill > 0 else ''}"
        )

    def save_svg(self, filepath: str | pathlib.Path):
        self._svg.save_svg(filepath)
