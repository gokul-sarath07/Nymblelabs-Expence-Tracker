from django.urls import path

from . import views

"""Url patterns for the Report views"""
urlpatterns = [
    path('', views.stats_view, name="stats"),
    path('category-summery', views.category_summery, name="category-summery"),
    path('weekly-summery', views.weekly_summery, name="weekly-summery"),
]
