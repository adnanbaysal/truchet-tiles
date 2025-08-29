from collections import defaultdict
from truchet_tiles.common.number_triangle import NumberTriangle


def triangle_to_subsquare(
    triangle: NumberTriangle,
) -> defaultdict[tuple[int, int], int]:
    # Puts the rows of the triangle into anti-diagonals starting from the top left
    # Then crops the nxn subsquare from the anti-diagonals.
    # Number of rows should be 2n or 2n - 1 to get a nxn square
    height = len(triangle.as_rows)
    height = height if height % 2 == 1 else height - 1
    n = (height + 1) // 2

    subsquare: defaultdict[tuple[int, int], int] = defaultdict(int)
    for col in range(n):
        for row in range(n):
            subsquare[(row, col)] = triangle.as_rows[row + col][col]

    return subsquare


def triangle_to_reflected_square(
    triangle: NumberTriangle,
) -> defaultdict[tuple[int, int], int]:
    # Puts the rows of the triangle into anti-diagonals starting from the top left
    # Then reflects the triangle along the main diagonal of the square.
    # If there are n rows, the square will be n x n
    n = len(triangle.as_rows)

    reflected_square: defaultdict[tuple[int, int], int] = defaultdict(int)

    # Fill the reflected_square with triangle.as_rows in anti-diagonal order
    for row in range(n):
        for col in range(row + 1):
            reflected_square[(row - col, col)] = triangle.as_rows[row][col]

    # Mirror the values along the main diagonal
    for row in range(1, n):
        for col in range(n - row, n):
            reflected_square[(row, col)] = reflected_square[(n - 1 - col, n - 1 - row)]

    return reflected_square
