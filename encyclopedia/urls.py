from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:keyword>", views.title, name="title"),
    path("error", views.entry_error, name="entry_error"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random", views.random_entry, name="random")
]
