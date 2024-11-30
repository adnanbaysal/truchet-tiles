from django import forms  # type: ignore

from truchet_tiles.common.enum import Connector
from truchet_tiles.rectangular.grid_generator import RectGridType
from truchet_tiles.rectangular.draw.enum import RectAnimationMethod

connectors = [(con.value.upper(), con.value.upper()) for con in Connector]
grid_types = [(gt.value.upper(), gt.value.upper()) for gt in RectGridType]
animation_methods = [(m.value, m.value.replace("_", " ")) for m in RectAnimationMethod]


class RectTilingForm(forms.Form):
    function = forms.ChoiceField(
        choices=grid_types,
        initial=RectGridType.XOR.value.upper(),
        widget=forms.Select(attrs={"onchange": "submit();"}),
        required=False,
    )
    align_to_axis = forms.BooleanField(
        initial=False,
        widget=forms.CheckboxInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    fill = forms.BooleanField(
        initial=False,
        widget=forms.CheckboxInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    invert_colors = forms.BooleanField(
        initial=False,
        widget=forms.CheckboxInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    connector = forms.ChoiceField(
        choices=connectors,
        initial=Connector.straight.value,
        widget=forms.Select(attrs={"onchange": "submit();"}),
        required=False,
    )
    hybrid_mode = forms.ChoiceField(
        choices=[(0, "None"), (1, "Mode 1"), (2, "Mode 2")],
        initial=0,
        widget=forms.Select(attrs={"onchange": "submit();"}),
        required=False,
    )
    animate = forms.BooleanField(
        initial=False,
        widget=forms.CheckboxInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    animation_method = forms.ChoiceField(
        choices=animation_methods,
        initial=RectAnimationMethod.at_once.value,
        widget=forms.Select(attrs={"onchange": "submit();"}),
        required=False,
    )
    show_grid = forms.BooleanField(
        initial=False,
        widget=forms.CheckboxInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    line_width = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=32,
        widget=forms.NumberInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    dimension = forms.IntegerField(
        initial=8,
        min_value=1,
        max_value=512,
        widget=forms.NumberInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    tile_size = forms.IntegerField(
        initial=32,
        min_value=6,
        max_value=512,
        widget=forms.NumberInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    animation_duration = forms.FloatField(
        initial=1.0,
        min_value=0.01,
        max_value=10.0,
        widget=forms.NumberInput(attrs={"onchange": "submit();", "step": "0.1"}),
        required=False,
    )
