from random import randint

from django.shortcuts import render
from django.http.request import HttpRequest

from truchet_tiles.web_ui.rectangular_tiling.forms import RectTilingForm
from truchet_tiles.rectangular.tiling import get_rectangular_tiling


def index(request: HttpRequest):
    if request.method == "POST":
        form = RectTilingForm(request.POST)
        if not form.is_valid():
            raise Exception(f"Invalid form: {form.errors}")

        cleaned_data = form.cleaned_data

        rand_seed = int(request.COOKIES.get("X-TRUCHET-TILING-SEED"))
        svg_text = get_rectangular_tiling(
            function=cleaned_data["function"],
            align_to_axis=cleaned_data["align_to_axis"],
            fill=cleaned_data["fill"],
            invert_colors=int(cleaned_data["invert_colors"]),
            curved=cleaned_data["curved"],
            hybrid_mode=int(cleaned_data["hybrid_mode"]),
            animate=cleaned_data["animate"],
            animation_method=cleaned_data["animation_method"],
            show_grid=cleaned_data["show_grid"],
            line_width=cleaned_data["line_width"],
            dimension=cleaned_data["dimension"],
            tile_size=cleaned_data["tile_size"],
            animation_duration=float(cleaned_data["animation_duration"]),
            rand_seed=rand_seed,
        )
    else:
        rand_seed = randint(0, 1 << 32)
        form = RectTilingForm()
        svg_text = get_rectangular_tiling(rand_seed=rand_seed)

    response = render(
        request,
        "rectangular_tiling/rect.html",
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
        "rectangular_tiling/base_empty.html"
        if "X-Requested-With" in request.headers
        and request.headers["X-Requested-With"] == "XMLHttpRequest"
        else "rectangular_tiling/base.html"
    )
