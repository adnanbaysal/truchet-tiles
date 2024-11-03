import datetime
import sys

import pygame

from truchet_tiles.rectangular.draw import TilingDrawer
from truchet_tiles.rectangular.grid_generator import GridGenerator, GridType


def interactive_display(grid_size: int, tile_size: int):
    clock = pygame.time.Clock()
    fps = 60

    grid_type = GridType.XOR
    grid_generator = GridGenerator(grid_size, grid_type)
    grid = grid_generator.get_grid()

    drawer = TilingDrawer(grid=grid, tile_size=tile_size)
    pygame.display.set_caption(grid_type)
    drawer.draw()

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    # Redraws screen. Has effect in random tiling
                    drawer.update_grid(grid_generator.get_grid())
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    grid_func = (
                        grid_generator.get_next_grid
                        if event.key == pygame.K_UP
                        else grid_generator.get_prev_grid
                    )
                    drawer.update_grid(grid_func())
                    drawer.draw()
                    pygame.display.set_caption(grid_generator.get_grid_type())
                elif event.key == pygame.K_m:
                    drawer.invert_animate()
                elif event.key == pygame.K_n:
                    drawer.next_animation_mode()
                elif event.key == pygame.K_c:
                    drawer.invert_curved()
                elif event.key == pygame.K_i:
                    drawer.invert_color()
                elif event.key == pygame.K_a:
                    drawer.invert_aligned()
                elif event.key == pygame.K_f:
                    drawer.invert_filled()
                elif event.key == pygame.K_g:
                    drawer.invert_show_grid_lines()
                elif event.key == pygame.K_h:
                    drawer.next_hybrid_mode()
                elif event.key == pygame.K_w:
                    drawer.increase_line_width()
                elif event.key == pygame.K_s:
                    drawer.decrease_line_width()
                elif event.key == pygame.K_p:
                    now_str = str(datetime.datetime.now())
                    tiling_identifier = drawer.tiling_identifier()
                    filename = (
                        f"output/"
                        f"{grid_type.value}_"
                        f"{tiling_identifier}_"
                        f"{now_str}"
                        f".svg"
                    )
                    drawer.save_svg(filename)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)


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

    interactive_display(grid_size=grid_size, tile_size=tile_size)
