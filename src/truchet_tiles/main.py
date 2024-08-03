import datetime
import sys

import pygame

from truchet_tiles.tiler import TruchetTiler
from truchet_tiles.grid_generator import generate_grid, GridType


def interactive_display(
        grid_type: GridType, grid_size: int, tile_size: int, angled: bool, filled: bool
    ):
    clock = pygame.time.Clock()
    fps = 60

    line_widths = tuple(i for i in range(1, 64))
    line_width_index = 2

    grid_types = [g.value for g in GridType]
    grid_type_index = grid_types.index(grid_type.value)
    
    color = 0
    grid = generate_grid(grid_size, grid_type)
    tiler = TruchetTiler(grid, tile_size, angled, color)
    pygame.display.set_caption(grid_type)
    draw_func = tiler.draw_filled if filled else tiler.draw_linear
    draw_func()
    
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    # invert colors
                    color = color ^ 1
                    tiler.color = color
                    draw_func()
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    # Redraws screen. Useful for random tiling
                    grid = generate_grid(grid_size, grid_type)
                    tiler.grid = grid
                    draw_func()
                elif event.key == pygame.K_p:
                    now_str = str(datetime.datetime.now())
                    pygame.image.save(tiler.screen, f"screenshot_{now_str}.jpeg")
                elif event.key == pygame.K_UP:
                    grid_type_index = (grid_type_index + 1) % len(grid_types)
                    grid_type = grid_types[grid_type_index]
                    grid = generate_grid(grid_size, grid_type)
                    tiler.grid = grid
                    draw_func()
                    pygame.display.set_caption(grid_type)
                elif event.key == pygame.K_DOWN:
                    grid_type_index = (grid_type_index - 1) % len(grid_types)
                    grid_type = grid_types[grid_type_index]
                    grid = generate_grid(grid_size, grid_type)
                    tiler.grid = grid
                    draw_func()
                    pygame.display.set_caption(grid_type)
                elif event.key == pygame.K_a:
                    tiler.angled = tiler.angled ^ True
                    draw_func()
                elif event.key == pygame.K_f:
                    filled = filled ^ True
                    draw_func = tiler.draw_filled if filled else tiler.draw_linear
                    draw_func()
                elif event.key == pygame.K_w:
                    line_width_index = (line_width_index + 1) % len(line_widths)
                    tiler.line_width = line_widths[line_width_index]
                    draw_func()
                elif event.key == pygame.K_s:
                    line_width_index = (line_width_index - 1) % len(line_widths)
                    tiler.line_width = line_widths[line_width_index]
                    draw_func()

        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    """ Usage: python main.py grid_size tile_size grid_func alignment mode
               any last-n parameter can be omitted.
        Arguments:
            grid_size: positive integer
            tile_size: positive integer
            grid_func: One of "xor", "mod", "multxor", "powxor", "sumxor", "random"
            alignment: one of "perp" or "angl"
            mode: one of "fill" or "line"

        Sample calls:
            64 16 xor perp fill
            64 16 mod angl line
    """
    pygame.init()

    grid_size = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    tile_size = int(sys.argv[2]) if len(sys.argv) > 2 else 56
    grid_type = GridType[sys.argv[3].upper()] if len(sys.argv) > 3 else GridType.XOR
    angled = sys.argv[4] == "angl" if len(sys.argv) > 4 else True
    filled = sys.argv[5] == "fill" if len(sys.argv) > 5 else False

    interactive_display(grid_type, grid_size, tile_size, angled, filled)
