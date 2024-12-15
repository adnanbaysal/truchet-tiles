import copy
from random import randint

from django.shortcuts import render  # type: ignore
from django.http.request import HttpRequest  # type: ignore

from truchet_tiles.web_ui.rectangular_tiling.forms import (
    INITIAL_TILING_VALUES,
    RectTilingForm,
)
from truchet_tiles.rectangular.tiling import get_rectangular_tiling


def index(request: HttpRequest):
    if request.method == "POST":
        form = RectTilingForm(request.POST)
        if not form.is_valid():
            raise Exception(f"Invalid form: {form.errors}")

        cleaned_data = form.cleaned_data

        image_height = cleaned_data["image_height"]
        dimension = cleaned_data["dimension"]
        edge_length = image_height / dimension

        rand_seed = int(request.COOKIES.get("X-TRUCHET-TILING-SEED"))
        svg_text = get_rectangular_tiling(
            function=cleaned_data["function"],
            align_to_axis=cleaned_data["align_to_axis"],
            fill_color=cleaned_data["fill_color"],
            line_color=cleaned_data["line_color"],
            bg_color=cleaned_data["bg_color"],
            connector=cleaned_data["connector"].lower(),
            hybrid_mode=int(cleaned_data["hybrid_mode"]),
            animate=cleaned_data["animate"],
            animation_method=cleaned_data["animation_method"],
            show_grid=cleaned_data["show_grid"],
            grid_line_width=cleaned_data["grid_line_width"],
            grid_color=cleaned_data["grid_color"],
            line_width=cleaned_data["line_width"],
            dimension=cleaned_data["dimension"],
            edge_length=edge_length,
            animation_duration=float(cleaned_data["animation_duration"]),
            rand_seed=rand_seed,
        )
    else:
        rand_seed = randint(0, 1 << 32)
        form = RectTilingForm()
        tiling_initial_values = copy.copy(INITIAL_TILING_VALUES)
        image_height = tiling_initial_values.pop("image_height")
        dimension = tiling_initial_values["dimension"]
        edge_length = image_height / dimension
        tiling_initial_values["edge_length"] = edge_length
        svg_text = get_rectangular_tiling(rand_seed=rand_seed, **tiling_initial_values)

    response = render(
        request,
        "rectangular_tiling/viewer.html",
        context={
            "template": _base_template(request),
            "form": form,
            "svg_text": svg_text,
        },
    )
    response.set_cookie("X-TRUCHET-TILING-SEED", rand_seed)

    return response


def _base_template(request):
    return (
        "base_empty.html"
        if "X-Requested-With" in request.headers
        and request.headers["X-Requested-With"] == "XMLHttpRequest"
        else "base.html"
    )
