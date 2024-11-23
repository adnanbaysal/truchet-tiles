import pathlib
import drawsvg as dw  # type: ignore

from truchet_tiles.hexagonal.draw.enum import (
    AnimationMethod,
    Colors,
    HexTop,
    Connector,
    Filledness,
    HybridFill,
    TilingColor,
)
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
        grid_dimension: int,
        grid: dict[tuple[int, int], int],
        edge_length: int,
        max_line_width: int = 32,
        flat_top: bool = False,
        fill: bool = False,
        invert_colors: bool = False,
        connector: str = "straight",
        hybrid_mode: int = 0,
        animate: bool = False,
        animation_method: str = "at_once",
        show_grid: bool = False,
        line_width: int = 1,
        animation_duration: float = 1.0,
    ) -> None:
        assert grid_dimension > 0, "grid_dimension must be positive"
        self._grid_dimension = grid_dimension

        assert len(grid) == 1 + sum(6 * i for i in range(grid_dimension))

        assert edge_length > 0, "edge_length must be positive"
        self._edge_length = edge_length
        self._draw_size = 2 * (2 * self._grid_dimension - 1) * self._edge_length

        self._orientation_name = HexTop.flat if flat_top else HexTop.pointy
        self._orientation = ORIENTATIONS[self._orientation_name]
        self._grid = grid
        self._hex_grid = (
            self._calculate_hex_grid()
        )  # NOTE: grid should be updated if orientation changed

        self._max_line_width = max_line_width
        self._line_width = line_width

        self._fill_style = Filledness.filled if fill else Filledness.linear
        self._connector = Connector(connector)
        self._tiling_color = TilingColor(invert_colors)
        self._hybrid_fill = HybridFill(hybrid_mode)

        self._show_grid_lines = show_grid

        self._animate = animate
        self._animation_method = AnimationMethod(animation_method)
        self._animation_prev_grid = {
            key: 0 for key in grid
        }  # TODO: Add hex grid versionæ
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
            edge_length, max_line_width=self._max_line_width
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
        # TODO: Fix svg to png issue on windows
        self._clear_screan()

        if self._fill_style == Filledness.linear:
            self._draw_linear()
        else:
            self._draw_filled()

        if self._show_grid_lines:
            self._draw_grid_lines()

        self._update_svg()

    def update_grid(
        self, grid: dict[tuple[int, int], int], set_current_to_prev: bool = False
    ):
        if set_current_to_prev:
            self._animation_prev_grid = self._grid

        self._grid = grid
        self._hex_grid = self._calculate_hex_grid()
        self.draw()

    def next_hybrid_mode(self):
        hybrid_before = self._hybrid_fill.value
        hybrid_after = (hybrid_before + 1) % 3
        self._hybrid_fill = HybridFill(hybrid_after)
        self.draw()

    def invert_color(self):
        self._tiling_color = (
            TilingColor.base
            if self._tiling_color == TilingColor.inverted
            else TilingColor.inverted
        )
        self.draw()

    def increase_line_width(self):
        self._line_width = (
            self._line_width + 1 if self._line_width != self._max_line_width else 1
        )
        self.draw()

    def decrease_line_width(self):
        self._line_width = (
            self._line_width - 1 if self._line_width != 1 else self._max_line_width
        )
        self.draw()

    def invert_orientation(self):
        self._orientation_name = (
            HexTop.flat if self._orientation_name == HexTop.pointy else HexTop.pointy
        )
        self._orientation = ORIENTATIONS[self._orientation_name]
        self._hex_grid = self._calculate_hex_grid()
        self.draw()

    def next_connector(self):
        self._connector = (
            Connector.curved
            if self._connector == Connector.straight
            else Connector.twoline
            if self._connector == Connector.curved
            else Connector.straight
        )
        self.draw()

    def invert_filled(self):
        self._fill_style = (
            Filledness.filled
            if self._fill_style == Filledness.linear
            else Filledness.linear
        )
        self.draw()

    def invert_show_grid_lines(self):
        self._show_grid_lines = self._show_grid_lines ^ True
        self.draw()

    def tiling_identifier(self) -> str:
        return (
            f"{self._grid_dimension}x{self._edge_length}px_"
            f"{'filled' if self._fill_style == Filledness.filled else 'line'}_"
            f"{self._connector.value}_"
            f"{'flat' if self._orientation_name == HexTop.flat else 'pointy'}_"
            f"w{self._line_width}_"
            f"{'hybrid' + str(self._hybrid_fill.value) + '_'}"
            f"{'anim_' + str(self._animation_method.value)}"
        )

    def save_svg(self, filepath: str | pathlib.Path):
        self._svg.save_svg(filepath)

    def invert_animate(self):
        self._animate ^= True
        self.draw()

    def set_rotation_duration(self, dur: float):
        self._animation_rotation_dur = dur
        self.draw()

    def set_animation_method(self, method: str):
        self._animation_method = AnimationMethod(method)
        self.draw()

    def next_animation_mode(self):
        if self._animation_method == AnimationMethod.at_once:
            self._animation_method = AnimationMethod.by_row
        elif self._animation_method == AnimationMethod.by_row:
            self._animation_method = AnimationMethod.by_tile
        else:
            self._animation_method = AnimationMethod.at_once

        self.draw()

    def _draw_linear(self):
        anim_start = self.ANIMATION_BEGIN
        for hex_, hex_data in self._hex_grid.items():
            self._insert_linear_tile(hex_, hex_data, anim_start)

            if self._animation_method == AnimationMethod.by_tile:
                if self._hex_grid[hex_].value != self._animation_prev_grid[hex_]:
                    anim_start += self._animation_rotation_dur

    def _clear_screan(self):
        self._svg.clear()
        self._svg = dw.Drawing(
            self._draw_size, self._draw_size, id_prefix="truchet_tiling"
        )
        self._svg_top_group = dw.Group(id="truchet_group", fill="none")
        # The following is the white background for svg
        self._svg_top_group.append(
            dw.Lines(
                -self._draw_size / 2,
                -self._draw_size / 2,
                -self._draw_size / 2,
                +self._draw_size / 2,
                +self._draw_size / 2,
                +self._draw_size / 2,
                +self._draw_size / 2,
                -self._draw_size / 2,
                stroke=Colors.SVG_WHITE,
                fill=Colors.SVG_WHITE,
                close=True,
            )
        )

    def _get_transform(self):
        # return (
        #     f"matrix(.5 -.5 .5 .5 0 {self._t_end * self._grid_size / 2})"
        #     if self._orientation_name == HexTop.flat
        #     else None
        # )
        return None

    def _update_svg(self):
        kwargs = {}
        transform = self._get_transform()

        self._svg.view_box = (
            -self._draw_size / 2,
            -self._draw_size / 2,
            self._draw_size,
            self._draw_size,
        )

        if transform:
            kwargs["transform"] = transform
            self._svg.view_box = (
                self._draw_size / 4,
                self._draw_size / 4,
                self._draw_size / 2,
                self._draw_size / 2,
            )

        self._svg.set_render_size()
        self._svg.append(dw.Use(self._svg_top_group, 0, 0, **kwargs))

    def _insert_linear_tile(self, hex_: Hex, hex_data: HexGridData, anim_start: float):
        used_tile = dw.Use(
            self._base_tiles[self._orientation_name][Filledness.linear][
                self._connector
            ][self._line_width][hex_data.value],
            hex_data.center.x,
            hex_data.center.y,
        )
        if self._animate and (
            self._animation_prev_grid[(hex_.q, hex_.r)] != self._grid[(hex_.q, hex_.r)]
        ):

            def _get_rotation(begin, dur, start_deg, end_deg):
                return dw.AnimateTransform(
                    attributeName="transform",
                    begin=begin,
                    dur=dur,
                    type="rotate",
                    from_or_values=f"{start_deg} {hex_data.center.x} {hex_data.center.y}",
                    to=f"{end_deg} {hex_data.center.x} {hex_data.center.x}",
                    fill="freeze",
                    repeatCount="1",
                )

            # The following animation will make the svg appear to start from the prev state
            used_tile.append_anim(
                _get_rotation(self.ANIMATION_DELAY, self.ANIMATION_DELAY, 0, 90)
            )
            used_tile.append_anim(
                _get_rotation(anim_start, self._animation_rotation_dur, 90, 180)
            )

        self._svg_top_group.append(used_tile)

    def _draw_filled(self):
        grid_of_fill_side = self._generate_fill_inside_grid()

        for grid_row in range(self._grid_size):
            y_offset = grid_row * self._t_end
            for grid_col in range(self._grid_size):
                x_offset = grid_col * self._t_end

                base_tile_index = (
                    self._hex_grid[grid_row][grid_col]
                    + 2 * grid_of_fill_side[grid_row][grid_col]
                )

                if self._connector == Connector.straight:
                    self._insert_filled_straight_tile(
                        x_offset, y_offset, base_tile_index
                    )
                else:
                    self._insert_filled_curved_tile(x_offset, y_offset, base_tile_index)

    def _generate_fill_inside_grid(self) -> list[list[int]]:
        _grid: list[list[int]] = []
        for grid_row in range(self._grid_size):
            _grid.append([])
            for grid_col in range(self._grid_size):
                neighbor = self._neighbor_cell(self._hex_grid, grid_row, grid_col)
                bit_changed = self._hex_grid[grid_row][grid_col] ^ neighbor
                if grid_row == 0 and grid_col == 0:
                    neighbor_fill = self._hex_grid[0][0] ^ self._tiling_color.value
                else:
                    neighbor_fill = self._neighbor_cell(_grid, grid_row, grid_col)
                _grid[grid_row].append(neighbor_fill ^ bit_changed ^ 1)

        return _grid

    @staticmethod
    def _neighbor_cell(_grid: list[list[int]], row: int, col: int) -> int:
        if row == 0 and col == 0:
            return _grid[row][col]
        if col > 0:
            return _grid[row][col - 1]
        if row > 0:
            return _grid[row - 1][col]
        raise ValueError("Invalid row and column")

    def _insert_filled_straight_tile(
        self, x_offset: int, y_offset: int, tile_index: int
    ):
        self._svg_top_group.append(
            dw.Use(
                self._base_tiles[Filledness.filled][Connector.straight][tile_index],
                x_offset,
                y_offset,
            )
        )

    def _insert_filled_curved_tile(self, x_offset: int, y_offset: int, tile_index: int):
        outside = tile_index < 2
        inside = tile_index > 1
        h_not_2 = self._hybrid_fill in (HybridFill.none, HybridFill.hybrid_1)
        h_not_1 = self._hybrid_fill in (HybridFill.none, HybridFill.hybrid_2)
        inverted = self._tiling_color == TilingColor.base

        if (
            (inside and h_not_2 and inverted)
            or (outside and h_not_1 and inverted)
            or (inside and h_not_1 and not inverted)
            or (outside and h_not_2 and not inverted)
        ):
            self._svg_top_group.append(
                dw.Use(
                    self._base_tiles[Filledness.filled][Connector.curved][tile_index],
                    x_offset,
                    y_offset,
                )
            )
        else:
            self._svg_top_group.append(
                dw.Use(
                    self._base_tiles[Filledness.filled][Connector.straight][tile_index],
                    x_offset,
                    y_offset,
                )
            )

    def _draw_grid_lines(self):
        for i in range(self._grid_size + 1):
            self._svg_top_group.append(
                dw.Line(
                    0,
                    i * self._t_end,
                    self._draw_size,
                    i * self._t_end,
                    stroke=Colors.SVG_RED,
                )
            )
            self._svg_top_group.append(
                dw.Line(
                    i * self._t_end,
                    0,
                    i * self._t_end,
                    self._draw_size,
                    stroke=Colors.SVG_RED,
                )
            )
