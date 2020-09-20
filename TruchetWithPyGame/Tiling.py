import pygame
from MandelbrotBinaryGrid import mandelbrot_binary_grid
from random import randint


def draw_tiles(grid, grid_size, tile_size):
    """ Draws the binary list of lists grid which is of square shape (n-rows and n-columns) """
    window_size = grid_size * tile_size
    tile_mid = int(tile_size / 2)
    screen = pygame.display.set_mode((window_size, window_size))
    background_colour = (255, 255, 255)
    screen.fill(background_colour)
    for grid_row in range(grid_size):
        y_offset = grid_row * tile_size
        for grid_col in range(grid_size):
            x_offset = grid_col * tile_size
            left1 = (x_offset, y_offset + tile_mid)
            left2 = (x_offset + tile_mid, y_offset + tile_size)
            right1 = (x_offset + tile_size, y_offset + tile_mid)
            right2 = (x_offset + tile_mid, y_offset)
            if grid[grid_row][grid_col] == 1:
                left2 = (x_offset + tile_mid, y_offset)
                right2 = (x_offset + tile_mid, y_offset + tile_size)
            pygame.draw.aaline(screen, (255, 0, 0), left1, left2, 1)
            pygame.draw.aaline(screen, (255, 0, 0), right1, right2, 1)
    pygame.display.flip()


def mandelbrot_tiling(grid_size=41, tile_size=8):
    """ Draws a binary mandelbrot grid with tiling
        grid_size is the number of tiler per row and column
        tile_size is the pixel size of each tile square"""
    grid = mandelbrot_binary_grid(grid_size)
    draw_tiles(grid, grid_size, tile_size)


def parity(x):
    par = 0
    while x != 0:
        par ^= x & 1
        x = int(x / 2)
    return par


def xor_tiling(grid_size=64, tile_size=16):
    grid = [[parity(x ^ y) for x in range(grid_size)] for y in range(grid_size)]
    draw_tiles(grid, grid_size, tile_size)


def random_tiling(grid_size=64, tile_size=16):
    grid = [[randint(0,1) for _ in range(grid_size)] for _ in range(grid_size)]
    draw_tiles(grid, grid_size, tile_size)


if __name__ == "__main__":
    # mandelbrot_tiling(grid_size=101)
    # xor_tiling()
    random_tiling()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
