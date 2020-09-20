from Complex import *


def is_mandelbrot_point(c, iteration=100, divergence_val=200):
    """ Iterate z(0) = c, z(n+1) = z(n) * (z(n) + 1) up to iteration times.
        Mark as divergent if length(z(i)) > divergence_val at any iteration,
        else mark convergent"""
    z = c
    for _ in range(iteration):
        z = cadd(csquare(z), z)
        if z.re ** 2 + z.im ** 2 > divergence_val:
            return False
    return True


def mandelbrot_binary_grid(grid_size):
    """ Returns binary grid of size grid_size x grid_size as a list of lists
        Covered area in Complex plane is the central square of width 4, i.e
        the area inside (-2,2), (2,2), (2,-2), and (-2,-2)"""
    divider = float(grid_size-1) / 4.0
    grid = [[(-2.0 + x / divider, 2.0 - y / divider) for x in range(grid_size)] for y in range(grid_size)]
    mandelbrot = []
    for row in grid:
        mbrow = []
        for element in row:
            c = Complex(element[0], element[1])
            mbrow.append(int(is_mandelbrot_point(c)))
        mandelbrot.append(mbrow)
    return mandelbrot


if __name__ == "__main__":
    mb = mandelbrot_binary_grid(51)
    for row in mb:
        print(row)
