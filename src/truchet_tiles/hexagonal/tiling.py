import random

from functools import cache

from truchet_tiles.common.enum import SvgColors
from truchet_tiles.hexagonal.draw import HexTilingDrawer
from truchet_tiles.hexagonal.grid_generator import HexGridType, get_hex_grid


@cache
def get_hexagonal_tiling(
    function: str = "XSIGNMAG",
    flat_top: bool = True,
    connector: str = "twoline",
    hybrid_connector: str | None = None,
    animate: bool = False,
    animation_method: str = "at_once",
    show_grid: bool = False,
    line_width: int = 1,
    dimension: int = 8,
    edge_length: float = 32,
    animation_duration: float = 1.0,
    rand_seed: int = 0,
    grid_line_width: float = 0.5,
    line_color: str = SvgColors.BLACK,
    bg_color: str = SvgColors.WHITE,
    fill_color: str = SvgColors.BLACK,
    grid_color: str = SvgColors.RED,
) -> str | None:
    # NOTE: Use rand_seed to control when to create new tiling in random mode
    # Pass the same rand_seed to update visual settings of the existing random tiling
    random.seed(rand_seed)

    grid = get_hex_grid(dimension, HexGridType(function.lower()))

    drawer = HexTilingDrawer(
        dimension=dimension,
        grid=grid,
        edge_length=edge_length,
        flat_top=flat_top,
        connector=connector,
        hybrid_connector=hybrid_connector,
        animate=animate,
        animation_method=animation_method,
        animation_duration=animation_duration,
        show_grid=show_grid,
        line_width=line_width,
        grid_line_width=grid_line_width,
        line_color=line_color,
        bg_color=bg_color,
        fill_color=fill_color,
        grid_color=grid_color,
    )

    drawer.draw()
    return drawer.svg.as_svg()
