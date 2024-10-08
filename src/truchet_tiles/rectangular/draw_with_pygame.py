import math
import pygame
import pygame.gfxdraw


class DrawTruchetPygame:
    MAX_LINE_WIDTH = 64

    def __init__(self, grid: list[list[int]], tile_size: int) -> None:
        assert tile_size > 0, "tile_size must be positive"
        self._tile_size = tile_size
        self._tile_mid = int(self._tile_size / 2)

        self._angled = True
        self._curved = False
        self._color = 0

        self._fill_color = (0, 0, 0)
        self._line_color = (0, 0, 0)
        self._line_width = 3

        self._hybrid_fill = 0  # if > 0, mixes curved and straight fills

        self.grid = grid
        assert all(
            len(row) == len(self.grid) for row in grid
        ), "grid should have the same number of rows as the number of columns"

        self._grid_size = len(self.grid)
        self._draw_size = self._grid_size * self._tile_size
        self.screen = pygame.display.set_mode((self._draw_size / 2, self._draw_size / 2))
        self._draw_surface = pygame.Surface((self._draw_size, self._draw_size), pygame.SRCALPHA)
        self._draw_background = (255, 255, 255)

    def next_hybrid_mode(self):
        self._hybrid_fill = (self._hybrid_fill + 1) % 3

    def invert_color(self):
        self._color = self._color ^ 1

    def increase_line_width(self):
        self._line_width = self._line_width + 1 if self._line_width != self.MAX_LINE_WIDTH else 1

    def decrease_line_width(self):
        self._line_width = self._line_width - 1 if self._line_width != 1 else self.MAX_LINE_WIDTH

    def invert_angled(self):
        self._angled = self._angled ^ True

    def invert_curved(self):
        self._curved = self._curved ^ True

    def _clear_screan(self):
        self._draw_surface.fill(self._draw_background)

    def _show_screen(self):
        if not self._angled:
            self.screen.blit(
                pygame.transform.scale_by(
                    pygame.transform.rotate(self._draw_surface, 315),
                    math.sqrt(2) / 2,
                ), 
                self._draw_surface.get_rect(center=(self._draw_size / 4, self._draw_size / 4)),
            )
        else:
            self.screen.blit(
                pygame.transform.scale_by(
                    self._draw_surface, 
                    1 / 2
                ),
                (0, 0)
            )
        
        pygame.display.flip()

    def _draw_cell_straight(self, x_offset: int, y_offset: int, cell_value: int):
        left1 = (x_offset, y_offset + self._tile_mid)
        right1 = (x_offset + self._tile_size, y_offset + self._tile_mid)
        
        if cell_value == 1:
            left2 = (x_offset + self._tile_mid, y_offset)
            right2 = (x_offset + self._tile_mid, y_offset + self._tile_size)
        else:
            left2 = (x_offset + self._tile_mid, y_offset + self._tile_size)
            right2 = (x_offset + self._tile_mid, y_offset)

        pygame.draw.line(self._draw_surface, self._line_color, left1, left2, self._line_width)
        pygame.draw.line(self._draw_surface, self._line_color, right1, right2, self._line_width)

    def _draw_cell_curved(self, x_offset: int, y_offset: int, cell_value: int):
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

    def draw_linear(self):
        self._clear_screan()
        for grid_row in range(self._grid_size):
            y_offset = grid_row * self._tile_size
            for grid_col in range(self._grid_size):
                x_offset = grid_col * self._tile_size

                if self._curved:
                    self._draw_cell_curved(x_offset, y_offset, self.grid[grid_row][grid_col])
                else:
                    self._draw_cell_straight(x_offset, y_offset, self.grid[grid_row][grid_col])
                
        self._show_screen()

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

        if self._curved:
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
                neighbor = self._neighbor_cell(self.grid, grid_row, grid_col)
                bit_changed = self.grid[grid_row][grid_col] ^ neighbor
                if grid_row == 0 and grid_col == 0:
                    neighbor_fill = self.grid[0][0] ^ self._color
                else:
                    neighbor_fill = self._neighbor_cell(_grid, grid_row, grid_col)
                _grid[grid_row].append(neighbor_fill ^ bit_changed ^ 1)

        return _grid

    def draw_filled(self):
        self._clear_screan()
        grid_of_fill_inside = self._generate_fill_inside_grid()

        for grid_row in range(self._grid_size):
            y_offset = grid_row * self._tile_size
            for grid_col in range(self._grid_size):
                x_offset = grid_col * self._tile_size

                self._draw_filled_tile(
                    grid_of_fill_inside[grid_row][grid_col],
                    self.grid[grid_row][grid_col],
                    x_offset,
                    y_offset,
                )

        self._show_screen()
