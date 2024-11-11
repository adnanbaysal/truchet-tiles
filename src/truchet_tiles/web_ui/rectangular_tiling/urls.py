from django.urls import path
from . import views

urlpatterns = [path("", views.index, name="rectangular_tiling_index")]
