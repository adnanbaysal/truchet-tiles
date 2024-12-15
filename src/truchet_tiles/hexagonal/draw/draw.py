import drawsvg as dw  # type: ignore

from truchet_tiles.common.enum import (
    SvgColors,
    Connector,
    HybridFill,
)
from truchet_tiles.hexagonal.draw.enum import HexAnimationMethod, HexTop
from truchet_tiles.hexagonal.draw.tile_generator import HexTileGenerator
from truchet_tiles.hexagonal.hex_grid import (
    ORIENTATIONS,
    Hex,
    HexGrid,
    HexGridData,
    Layout,
    Point,
)


class HexTilingDrawer:
    ANIMATION_DELAY = "0.000001s"
    ANIMATION_BEGIN = 1.0

    def __init__(
        self,
        dimension: int,
        grid: dict[tuple[int, int], int],
        edge_length: int,
        flat_top: bool = False,
        connector: str = "twoline",
        hybrid_mode: int = 0,
        animate: bool = False,
        animation_method: str = "at_once",
        animation_duration: float = 0.5,
        show_grid: bool = False,
        line_width: int = 1,
        grid_line_width: float = 0.5,
        line_color: str = SvgColors.BLACK,
        bg_color: str = SvgColors.WHITE,
        fill_color: str = SvgColors.BLACK,
        grid_color: str = SvgColors.RED,
    ) -> None:
        assert dimension > 0, "dimension must be positive"
        self._dimension = dimension

        assert len(grid) == 1 + sum(6 * i for i in range(dimension))

        assert edge_length > 0, "edge_length must be positive"
        self._edge_length = edge_length
        self._draw_size = 2 * (2 * self._dimension - 1) * self._edge_length

        self._orientation_name = HexTop.flat if flat_top else HexTop.pointy
        self._orientation = ORIENTATIONS[self._orientation_name]
        self._grid = grid
        self._hex_grid = (
            self._calculate_hex_grid()
        )  # NOTE: grid should be updated if orientation changed

        self._line_width = line_width

        self._connector = Connector(connector)
        self._hybrid_fill = HybridFill(hybrid_mode)

        self._show_grid_lines = show_grid
        self._grid_line_width = grid_line_width
        self._grid_color = grid_color

        self._line_color = line_color
        self._bg_color = bg_color
        self._fill_color = fill_color

        self._animate = animate
        self._animation_method = HexAnimationMethod(animation_method)
        self._animation_prev_grid = {
            key: 0 for key in grid
        }  # TODO: Add hex grid version.
        self._animation_rotation_dur = animation_duration

        self._svg = dw.Drawing(
            self._draw_size,
            self._draw_size,
            origin=(0, 0),
            id_prefix="hex_truchet_tiling",
        )
        self._svg_top_group = dw.Group(
            id="truchet_group", fill="none"
        )  # To handle translations

        self._base_tiles = HexTileGenerator(
            edge_length,
            line_width=self._line_width,
            line_color=self._line_color,
            fill_color=self._fill_color,
            bg_color=self._bg_color,
            hex_top=self._orientation_name,
        )

    def _calculate_hex_grid(self) -> HexGrid:
        layout = Layout(
            orientation=self._orientation,
            size=Point(self._edge_length, self._edge_length),
            origin=Point(0, 0),
        )

        return HexGrid(hex_grid=self._grid, layout=layout)

    @property
    def svg(self):
        return self._svg

    def draw(self):
        self._clear_screan()
        self._draw()

        if self._show_grid_lines:
            self._draw_grid_lines()

        self._update_svg()

    def _clear_screan(self):
        self._svg.clear()
        self._svg = dw.Drawing(
            self._draw_size, self._draw_size, id_prefix="truchet_tiling"
        )
        self._svg_top_group = dw.Group(id="truchet_group", fill="none")

    def _update_svg(self):
        self._svg.view_box = (
            -self._draw_size / 2,
            -self._draw_size / 2,
            self._draw_size,
            self._draw_size,
        )

        self._svg.set_render_size()
        self._svg.append(dw.Use(self._svg_top_group, 0, 0, transform="scale(1.1)"))

    def _draw(self):
        anim_start = self.ANIMATION_BEGIN
        hex_index = 0

        for hex_, hex_data in self._hex_grid.items():
            coord = (hex_.q, hex_.r)

            if self._animate and self._grid[coord] != self._animation_prev_grid[coord]:
                if self._animation_method == HexAnimationMethod.by_tile:
                    anim_start = (
                        self.ANIMATION_BEGIN + hex_index * self._animation_rotation_dur
                    )
                elif self._animation_method == HexAnimationMethod.by_ring:
                    anim_start = (
                        self.ANIMATION_BEGIN + abs(hex_) * self._animation_rotation_dur
                    )
                elif self._animation_method == HexAnimationMethod.at_once:
                    anim_start = self.ANIMATION_BEGIN

            if self._connector == Connector.curved:
                used_tile = self._get_curved_tile(hex_data)
            else:
                used_tile = dw.Use(
                    self._base_tiles[self._connector][hex_data.value],
                    hex_data.center.x,
                    hex_data.center.y,
                )

            self._append_anims_to_tile(hex_, hex_data, used_tile, anim_start)
            self._svg_top_group.append(used_tile)

    def _append_anims_to_tile(
        self, hex_: Hex, hex_data: HexGridData, used_tile: dw.Use, anim_start: float
    ):
        if self._animate and (
            self._animation_prev_grid[(hex_.q, hex_.r)] != self._grid[(hex_.q, hex_.r)]
        ):
            self._append_rotation(hex_data, used_tile, anim_start)
            # TODO: Add color animation

    def _append_rotation(
        self, hex_data: HexGridData, used_tile: dw.Use, anim_start: float
    ):
        def _get_rotation(begin, dur, start_deg, end_deg):
            return dw.AnimateTransform(
                attributeName="transform",
                begin=begin,
                dur=dur,
                type="rotate",
                from_or_values=f"{start_deg} {hex_data.center.x} {hex_data.center.y}",
                to=f"{end_deg} {hex_data.center.x} {hex_data.center.y}",
                fill="freeze",
                repeatCount="1",
            )

        # The following animation will make the svg appear to start from the prev state
        used_tile.append_anim(
            _get_rotation(self.ANIMATION_DELAY, self.ANIMATION_DELAY, 0, 60)
        )
        used_tile.append_anim(
            _get_rotation(anim_start, self._animation_rotation_dur, 60, 120)
        )

    # TODO: Implement color animations

    def _get_curved_tile(self, hex_data: HexGridData):
        h_not_2 = self._hybrid_fill in (HybridFill.none, HybridFill.hybrid_1)
        h_not_1 = self._hybrid_fill in (HybridFill.none, HybridFill.hybrid_2)

        if (hex_data.value == 1 and h_not_2) or (hex_data.value == 0 and h_not_1):
            return dw.Use(
                self._base_tiles[Connector.curved][hex_data.value],
                hex_data.center.x,
                hex_data.center.y,
            )
        else:
            return dw.Use(
                self._base_tiles[Connector.line][hex_data.value],
                hex_data.center.x,
                hex_data.center.y,
            )

    def _draw_grid_lines(self):
        for hex_data in self._hex_grid.values():
            points = []
            for p in hex_data.corners:
                points += [p.x, p.y]

            self._svg_top_group.append(
                dw.Lines(
                    *points,
                    stroke=self._grid_color,
                    stroke_width=self._grid_line_width,
                    close=True,
                )
            )
