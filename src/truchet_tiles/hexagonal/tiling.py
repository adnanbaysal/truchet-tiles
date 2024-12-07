import random

from functools import cache

from truchet_tiles.hexagonal.draw import HexTilingDrawer
from truchet_tiles.hexagonal.grid_generator import HexGridGenerator, HexGridType


@cache
def get_hexagonal_tiling(
    function: str = "XSIGNMAG",
    flat_top: bool = True,
    fill: bool = False,
    invert_colors: bool = False,
    connector: str = "straight",
    hybrid_mode: int = 0,
    animate: bool = False,
    animation_method: str = "at_once",
    show_grid: bool = False,
    line_width: int = 1,
    dimension: int = 8,
    edge_length: int = 32,
    animation_duration: float = 1.0,
    rand_seed: int = 0,
) -> str | None:
    # NOTE: Use rand_seed to control when to create new tiling in random mode
    # Pass the same rand_seed to update visual settings of the existing random tiling
    random.seed(rand_seed)

    grid_generator = HexGridGenerator(dimension, HexGridType(function.lower()))
    grid = grid_generator.grid

    drawer = HexTilingDrawer(
        dimension=dimension,
        grid=grid,
        edge_length=edge_length,
        flat_top=flat_top,
        fill=fill,
        invert_colors=invert_colors,
        connector=connector,
        hybrid_mode=hybrid_mode,
        animate=animate,
        animation_method=animation_method,
        animation_duration=animation_duration,
        show_grid=show_grid,
        line_width=line_width,
    )

    drawer.draw()
    return drawer.svg.as_html()
