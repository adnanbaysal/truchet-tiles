from django import forms  # type: ignore

from truchet_tiles.common.enum import Connector
from truchet_tiles.hexagonal.grid_generator import HexGridType
from truchet_tiles.hexagonal.draw.enum import HexAnimationMethod

connectors = [(con.value.upper(), con.value.upper()) for con in Connector]
grid_types = [(gt.value.upper(), gt.value.upper()) for gt in HexGridType]
animation_methods = [(m.value, m.value.replace("_", " ")) for m in HexAnimationMethod]


INITIAL_TILING_VALUES = {
    "function": HexGridType.XSIGNMAG.value.upper(),
    "dimension": 8,
    "connector": Connector.twoline.value,
    "hybrid_mode": 0,
    "flat_top": True,
    "line_width": 2,
    "line_color": "#264653",
    "fill_color": "#F4A261",
    "bg_color": "#A8DADC",
    "animate": False,
    "animation_method": HexAnimationMethod.at_once.value,
    "animation_duration": 0.5,
    "show_grid": False,
    "grid_line_width": 0.5,
    "grid_color": "#FF0000",
    "image_height": 800,
}


class HexTilingForm(forms.Form):
    function = forms.ChoiceField(
        choices=grid_types,
        initial=INITIAL_TILING_VALUES["function"],
        widget=forms.Select(attrs={"onchange": "submit();"}),
        required=False,
    )
    dimension = forms.IntegerField(
        initial=INITIAL_TILING_VALUES["dimension"],
        min_value=1,
        max_value=64,
        widget=forms.NumberInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    connector = forms.ChoiceField(
        choices=connectors,
        initial=INITIAL_TILING_VALUES["connector"],
        widget=forms.Select(attrs={"onchange": "submit();"}),
        required=False,
    )
    hybrid_mode = forms.ChoiceField(
        choices=[(0, "None"), (1, "Mode 1"), (2, "Mode 2")],
        initial=INITIAL_TILING_VALUES["hybrid_mode"],
        widget=forms.Select(attrs={"onchange": "submit();"}),
        required=False,
    )
    flat_top = forms.BooleanField(
        initial=INITIAL_TILING_VALUES["flat_top"],
        widget=forms.CheckboxInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    line_width = forms.IntegerField(
        initial=INITIAL_TILING_VALUES["line_width"],
        min_value=1,
        max_value=32,
        widget=forms.NumberInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    line_color = forms.CharField(
        initial=INITIAL_TILING_VALUES["line_color"],
        max_length=20,
        widget=forms.TextInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    fill_color = forms.CharField(
        initial=INITIAL_TILING_VALUES["fill_color"],
        max_length=20,
        widget=forms.TextInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    bg_color = forms.CharField(
        initial=INITIAL_TILING_VALUES["bg_color"],
        max_length=20,
        widget=forms.TextInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    animate = forms.BooleanField(
        initial=INITIAL_TILING_VALUES["animate"],
        widget=forms.CheckboxInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    animation_method = forms.ChoiceField(
        choices=animation_methods,
        initial=INITIAL_TILING_VALUES["animation_method"],
        widget=forms.Select(attrs={"onchange": "submit();"}),
        required=False,
    )
    animation_duration = forms.FloatField(
        initial=INITIAL_TILING_VALUES["animation_duration"],
        min_value=0.01,
        max_value=10.0,
        widget=forms.NumberInput(attrs={"onchange": "submit();", "step": "0.1"}),
        required=False,
    )
    show_grid = forms.BooleanField(
        initial=INITIAL_TILING_VALUES["show_grid"],
        widget=forms.CheckboxInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    grid_line_width = forms.FloatField(
        initial=INITIAL_TILING_VALUES["grid_line_width"],
        min_value=0.01,
        max_value=5.0,
        widget=forms.NumberInput(attrs={"onchange": "submit();", "step": "0.1"}),
        required=False,
    )
    grid_color = forms.CharField(
        initial=INITIAL_TILING_VALUES["grid_color"],
        max_length=20,
        widget=forms.TextInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    image_height = forms.IntegerField(
        initial=INITIAL_TILING_VALUES["image_height"],
        min_value=200,
        max_value=10000,
        widget=forms.NumberInput(attrs={"onchange": "submit();"}),
        required=False,
    )
