from django.urls import path  # type: ignore
from . import views

urlpatterns = [path("", views.index, name="main_page_index")]
