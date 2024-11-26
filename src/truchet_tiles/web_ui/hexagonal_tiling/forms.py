from django import forms

from truchet_tiles.hexagonal.grid_generator import HexGridType
from truchet_tiles.hexagonal.draw.enum import AnimationMethod, Connector

connectors = [(con.value.upper(), con.value.upper()) for con in Connector]
grid_types = [(gt.value.upper(), gt.value.upper()) for gt in HexGridType]
animation_methods = [(m.value, m.value.replace("_", " ")) for m in AnimationMethod]


class HexTilingForm(forms.Form):
    function = forms.ChoiceField(
        choices=grid_types,
        initial=HexGridType.XSIGNMAG.value.upper(),
        widget=forms.Select(attrs={"onchange": "submit();"}),
        required=False,
    )
    flat_top = forms.BooleanField(
        initial=True,
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
        initial=AnimationMethod.at_once.value,
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
    grid_dimension = forms.IntegerField(
        initial=4,
        min_value=1,
        max_value=64,
        widget=forms.NumberInput(attrs={"onchange": "submit();"}),
        required=False,
    )
    edge_length = forms.IntegerField(
        initial=64,
        min_value=6,
        max_value=1024,
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
