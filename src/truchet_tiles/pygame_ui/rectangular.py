import datetime
import pathlib
import sys

import pygame

from truchet_tiles.rectangular.draw import RectTilingDrawer
from truchet_tiles.rectangular.grid_generator import RectGridGenerator, RectGridType


CURR_DIR = pathlib.Path(__file__).parent.resolve()


class RectPygameViewer:
    DISPLAY_FILE_PATH = (CURR_DIR / "truchet.png").as_posix()
    FPS = 60

    def __init__(self, grid_size: int, tile_size: int):
        self._grid_size = grid_size
        self._tile_size = tile_size
        self._draw_size = self._grid_size * self._tile_size
        self._screen = pygame.display.set_mode((self._draw_size, self._draw_size))
        self._clock = pygame.time.Clock()

        self._grid_type = RectGridType.XOR
        self._grid_generator = RectGridGenerator(self._grid_size, self._grid_type)
        self._grid = self._grid_generator.grid

        self._drawer = RectTilingDrawer(grid=self._grid, tile_size=self._tile_size)
        self._drawer.draw()

    def show_svg(self):
        self._drawer.svg.save_png(self.DISPLAY_FILE_PATH)
        self._draw_surface = pygame.image.load(self.DISPLAY_FILE_PATH)
        self._screen.blit(self._draw_surface, (0, 0))

    def interactive_display(self):
        self.show_svg()

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        # Redraws screen. Has effect in random tiling
                        self._drawer.update_grid(
                            self._grid_generator.get_grid_by_name(self._grid_type.value)
                        )
                        self.show_svg()
                    elif event.key in (pygame.K_UP, pygame.K_DOWN):
                        grid_func = (
                            self._grid_generator.get_next_grid
                            if event.key == pygame.K_UP
                            else self._grid_generator.get_prev_grid
                        )
                        self._drawer.update_grid(grid_func())
                        self.show_svg()
                        pygame.display.set_caption(self._grid_generator.get_grid_type())
                    elif event.key == pygame.K_m:
                        self._drawer.invert_animate()
                        self.show_svg()
                    elif event.key == pygame.K_n:
                        self._drawer.next_animation_mode()
                        self.show_svg()
                    elif event.key == pygame.K_c:
                        self._drawer.next_connector()
                        self.show_svg()
                    elif event.key == pygame.K_i:
                        self._drawer.invert_color()
                        self.show_svg()
                    elif event.key == pygame.K_a:
                        self._drawer.invert_aligned()
                        self.show_svg()
                    elif event.key == pygame.K_f:
                        self._drawer.invert_filled()
                        self.show_svg()
                    elif event.key == pygame.K_g:
                        self._drawer.invert_show_grid_lines()
                        self.show_svg()
                    elif event.key == pygame.K_h:
                        self._drawer.next_hybrid_mode()
                        self.show_svg()
                    elif event.key == pygame.K_w:
                        self._drawer.increase_line_width()
                        self.show_svg()
                    elif event.key == pygame.K_s:
                        self._drawer.decrease_line_width()
                        self.show_svg()
                    elif event.key == pygame.K_p:
                        now_str = str(datetime.datetime.now())
                        tiling_identifier = self._drawer.tiling_identifier()
                        filename = (
                            f"output/"
                            f"{self._grid_type.value}_"
                            f"{tiling_identifier}_"
                            f"{now_str}"
                            f".svg"
                        )
                        self._drawer.save_svg(filename)

            pygame.display.flip()
            pygame.display.update()
            self._clock.tick(self.FPS)


if __name__ == "__main__":
    """ Usage: python main.py grid_size tile_size
               0, 1, or 2 arguments can be given.
        Arguments:
            grid_size: positive integer, default 16
            tile_size: positive integer, default 50
    """
    pygame.init()

    grid_size = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    tile_size = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    RectPygameViewer(grid_size=grid_size, tile_size=tile_size).interactive_display()
