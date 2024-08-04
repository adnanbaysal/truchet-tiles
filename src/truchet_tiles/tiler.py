import math
import pygame
import pygame.gfxdraw


class TruchetTiler:
    def __init__(
        self,
        grid: list[list[int]],
        tile_size: int = 32,
        angled: bool = False,
        color = 0,
        line_color: tuple[int, int, int] = (0, 0, 0),
        line_width: int = 3,
    ) -> None:
        assert tile_size > 0, "tile_size must be positive"
        self.tile_size = tile_size
        self.tile_mid = int(self.tile_size / 2)

        self.angled = angled
        self.color = color

        self.line_color = line_color
        self.line_width = line_width

        self.grid = grid
        assert all(
            len(row) == len(self.grid) for row in grid
        ), "grid should have the same number of rows as the number of columns"

        self.grid_size = len(self.grid)
        self.draw_size = self.grid_size * self.tile_size
        self.screen = pygame.display.set_mode((self.draw_size / 2, self.draw_size / 2))
        self.draw_surface = pygame.Surface((self.draw_size, self.draw_size), pygame.SRCALPHA)
        self._draw_background = (255, 255, 255)

    def _clear_screan(self):
        self.draw_surface.fill(self._draw_background)

    def _show_screen(self):
        if not self.angled:
            self.screen.blit(
                pygame.transform.scale_by(
                    pygame.transform.rotate(self.draw_surface, 315),
                    math.sqrt(2) / 2,
                ), 
                self.draw_surface.get_rect(center=(self.draw_size / 4, self.draw_size / 4)),
            )
        else:
            self.screen.blit(
                pygame.transform.scale_by(
                    self.draw_surface, 
                    1 / 2
                ),
                (0, 0)
            )
        
        pygame.display.flip()

    def draw_linear(self):
        self._clear_screan()
        for grid_row in range(self.grid_size):
            y_offset = grid_row * self.tile_size
            for grid_col in range(self.grid_size):
                x_offset = grid_col * self.tile_size

                left1 = (x_offset, y_offset + self.tile_mid)
                left2 = (x_offset + self.tile_mid, y_offset + self.tile_size)
                right1 = (x_offset + self.tile_size, y_offset + self.tile_mid)
                right2 = (x_offset + self.tile_mid, y_offset)

                if self.grid[grid_row][grid_col] == 1:
                    left2 = (x_offset + self.tile_mid, y_offset)
                    right2 = (x_offset + self.tile_mid, y_offset + self.tile_size)

                pygame.draw.line(self.draw_surface, self.line_color, left1, left2, self.line_width)
                pygame.draw.line(self.draw_surface, self.line_color, right1, right2, self.line_width)
                
        self._show_screen()

    def _draw_filled_tile(
        self,
        fill_inside: int,
        rotate: int,
        x: int,
        y: int,
    ):
        middle = self.tile_mid
        end = self.tile_size

        if not fill_inside:
            # draw two triangles
            if not rotate:
                # left mid to top mid + bottom mid to right mid
                triangle1 = ((x, y), (x + middle, y), (x, y + middle))
                triangle2 = ((x + end, y + end), (x + middle, y + end), (x + end, y + middle))

            else:
                triangle1 = ((x + end, y), (x + end, y + middle), (x + middle, y))
                triangle2 = ((x, y + end), (x, y + middle), (x + middle, y + end))

            pygame.draw.polygon(self.draw_surface, self.line_color, triangle1, width=0)
            pygame.draw.polygon(self.draw_surface, self.line_color, triangle2, width=0)

        else:
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

            pygame.draw.polygon(self.draw_surface, self.line_color, points, width=0)

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
        for grid_row in range(self.grid_size):
            _grid.append([])
            for grid_col in range(self.grid_size):
                neighbor = self._neighbor_cell(self.grid, grid_row, grid_col)
                bit_changed = self.grid[grid_row][grid_col] ^ neighbor
                if grid_row == 0 and grid_col == 0:
                    neighbor_fill = self.grid[0][0] ^ self.color
                else:
                    neighbor_fill = self._neighbor_cell(_grid, grid_row, grid_col)
                _grid[grid_row].append(neighbor_fill ^ bit_changed ^ 1)

        return _grid

    def draw_filled(self):
        self._clear_screan()
        grid_of_fill_inside = self._generate_fill_inside_grid()

        for grid_row in range(self.grid_size):
            y_offset = grid_row * self.tile_size
            for grid_col in range(self.grid_size):
                x_offset = grid_col * self.tile_size

                self._draw_filled_tile(
                    grid_of_fill_inside[grid_row][grid_col],
                    self.grid[grid_row][grid_col],
                    x_offset,
                    y_offset,
                )

        self._show_screen()
