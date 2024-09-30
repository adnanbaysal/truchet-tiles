import datetime
import sys

import pygame

from truchet_tiles.rectangular.draw_with_pygame import DrawTruchetPygame
from truchet_tiles.rectangular.grid_generator import generate_grid, GridType


def interactive_display(grid_size: int, tile_size: int):
    clock = pygame.time.Clock()
    fps = 60

    grid_type = GridType.XOR
    grid_types = [g.value for g in GridType]
    grid_type_index = grid_types.index(grid_type.value)
    
    grid = generate_grid(grid_size, grid_type)
    drawer = DrawTruchetPygame(grid=grid, tile_size=tile_size)
    pygame.display.set_caption(grid_type)
    filled = False
    draw_func = drawer.draw_linear
    draw_func()
    
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    drawer.invert_color()
                    draw_func()
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    # Redraws screen. Useful for random tiling
                    grid = generate_grid(grid_size, grid_type)
                    drawer.grid = grid
                    draw_func()
                elif event.key == pygame.K_p:
                    now_str = str(datetime.datetime.now())
                    pygame.image.save(drawer.screen, f"screenshot_{now_str}.jpeg")
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    adder = +1 if event.key == pygame.K_UP else -1
                    grid_type_index = (grid_type_index + adder) % len(grid_types)
                    grid_type = grid_types[grid_type_index]
                    grid = generate_grid(grid_size, grid_type)
                    drawer.grid = grid
                    draw_func()
                    pygame.display.set_caption(grid_type)
                elif event.key == pygame.K_a:
                    drawer.invert_angled()
                    draw_func()
                elif event.key == pygame.K_f:
                    filled = filled ^ True
                    draw_func = drawer.draw_filled if filled else drawer.draw_linear
                    draw_func()
                elif event.key == pygame.K_w:
                    drawer.increase_line_width()
                    draw_func()
                elif event.key == pygame.K_s:
                    drawer.decrease_line_width()
                    draw_func()
                elif event.key == pygame.K_c:
                    drawer.invert_curved()
                    draw_func()
                elif event.key == pygame.K_h:
                    drawer.next_hybrid_mode()
                    draw_func()

        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    """ Usage: python main.py grid_size tile_size
               0, 1, or 2 arguments can be given.
        Arguments:
            grid_size: positive integer, default 32
            tile_size: positive integer, default 56
    """
    pygame.init()

    grid_size = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    tile_size = int(sys.argv[2]) if len(sys.argv) > 2 else 56

    interactive_display(grid_size=grid_size, tile_size=tile_size)
