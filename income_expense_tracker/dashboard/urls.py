from django.urls import path

from . import views

"""Url pattern for dashboard view."""
urlpatterns = [
    path('', views.index, name="home"),
]
