import copy
from random import randint

from django.shortcuts import render  # type: ignore
from django.http.request import HttpRequest  # type: ignore

from truchet_tiles.web_ui.hexagonal_tiling.forms import (
    INITIAL_TILING_VALUES,
    HexTilingForm,
)
from truchet_tiles.hexagonal.tiling import get_hexagonal_tiling


def index(request: HttpRequest):
    if request.method == "POST":
        form = HexTilingForm(request.POST)
        if not form.is_valid():
            raise Exception(f"Invalid form: {form.errors}")

        cleaned_data = form.cleaned_data

        rand_seed = int(request.COOKIES.get("X-TRUCHET-TILING-SEED"))
        image_height = cleaned_data["image_height"]
        dimension = cleaned_data["dimension"]
        edge_length = image_height / (2 * (2 * dimension - 1))

        svg_text = get_hexagonal_tiling(
            function=cleaned_data["function"],
            flat_top=cleaned_data["flat_top"],
            fill=cleaned_data["fill"],
            invert_colors=int(cleaned_data["invert_colors"]),
            connector=cleaned_data["connector"].lower(),
            hybrid_mode=int(cleaned_data["hybrid_mode"]),
            animate=cleaned_data["animate"],
            animation_method=cleaned_data["animation_method"],
            show_grid=cleaned_data["show_grid"],
            line_width=cleaned_data["line_width"],
            dimension=cleaned_data["dimension"],
            edge_length=edge_length,
            animation_duration=float(cleaned_data["animation_duration"]),
            rand_seed=rand_seed,
        )
    else:
        rand_seed = randint(0, 1 << 32)
        form = HexTilingForm()
        tiling_initial_values = copy.copy(INITIAL_TILING_VALUES)
        image_height = tiling_initial_values.pop("image_height")
        dimension = tiling_initial_values["dimension"]
        edge_length = image_height / (2 * (2 * dimension - 1))
        tiling_initial_values["edge_length"] = edge_length
        svg_text = get_hexagonal_tiling(rand_seed=rand_seed, **tiling_initial_values)

    response = render(
        request,
        "hexagonal_tiling/viewer.html",
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
