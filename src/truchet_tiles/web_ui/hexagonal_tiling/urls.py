from django.urls import path
from . import views

urlpatterns = [path("", views.index, name="hexagonal_tiling_index")]
