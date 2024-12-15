from django import forms  # type: ignore

from truchet_tiles.common.enum import Connector
from truchet_tiles.rectangular.grid_generator import RectGridType
from truchet_tiles.rectangular.draw.enum import RectAnimationMethod

connectors = [
    ("LINE", "LINE"),
    ("CURVED", "CURVED"),
    ("TWOLINE", "TWOLINE"),
]  # NOTE: Manually done to set the order
grid_types = [(gt.value.upper(), gt.value.upper()) for gt in RectGridType]
animation_methods = [(m.value, m.value.replace("_", " ")) for m in RectAnimationMethod]

INITIAL_TILING_VALUES = {
    "function": RectGridType.XOR.value.upper(),
    "align_to_axis": False,
    "fill_color": "#FFFFFF",
    "line_color": "#000000",
    "bg_color": "#FFFF00",
    "connector": Connector.line.value,
    "hybrid_mode": 0,
    "animate": False,
    "animation_method": RectAnimationMethod.at_once.value,
    "animation_duration": 0.5,
    "show_grid": False,
    "grid_line_width": 0.5,
    "grid_color": "#FF0000",
    "line_width": 1,
    "dimension": 5,
    "image_height": 720,
}


class RectTilingForm(forms.Form):
    function = forms.ChoiceField(
        choices=grid_types,
        initial=INITIAL_TILING_VALUES["function"],
        widget=forms.Select(attrs={"onchange": "submit();"}),
        required=False,
    )
    dimension = forms.IntegerField(
        initial=INITIAL_TILING_VALUES["dimension"],
        min_value=1,
        max_value=512,
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
    align_to_axis = forms.BooleanField(
        initial=INITIAL_TILING_VALUES["align_to_axis"],
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
        min_value=128,
        max_value=10000,
        widget=forms.NumberInput(attrs={"onchange": "submit();"}),
        required=False,
    )
