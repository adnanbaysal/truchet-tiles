from django.shortcuts import render  # type: ignore
from django.http.request import HttpRequest  # type: ignore


def index(request: HttpRequest):
    return render(
        request,
        "main_page/main.html",
    )
