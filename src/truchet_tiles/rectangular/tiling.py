from functools import cache

from truchet_tiles.rectangular.draw import TilingDrawer
from truchet_tiles.rectangular.grid_generator import GridGenerator, GridType


@cache
def get_rectangular_tiling(
    function: str = "XOR",
    align_to_axis: bool = False,
    fill: bool = False,
    invert_colors: bool = False,
    curved: bool = False,
    hybrid_mode: int = 0,
    animate: bool = False,
    animation_method: str = "at_once",
    show_grid: bool = False,
    line_width: int = 1,
    dimension: int = 8,
    tile_size: int = 32,
    animation_duration: float = 1.0,
    rand_seed: int = 0,
) -> str:
    # NOTE: Use rand_seed to control when to create new tiling in random mode
    # Pass the same rand_seed to update visual settings of the existing random tiling

    grid_generator = GridGenerator(dimension, GridType(function.lower()))
    grid = grid_generator.get_grid()

    drawer = TilingDrawer(
        grid=grid,
        tile_size=tile_size,
        align_to_axis=align_to_axis,
        fill=fill,
        invert_colors=invert_colors,
        curved=curved,
        hybrid_mode=hybrid_mode,
        animate=animate,
        animation_method=animation_method,
        show_grid=show_grid,
        line_width=line_width,
        animation_duration=animation_duration,
    )

    drawer.draw()
    return drawer.svg.as_html()
