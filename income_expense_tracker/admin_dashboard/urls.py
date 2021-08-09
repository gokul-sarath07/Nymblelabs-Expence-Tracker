from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

"""Url pattern for admin dashboard view."""
urlpatterns = [
    path('', views.index, name="admin_dashboard"),
    path('filter-users', csrf_exempt(views.filter_users), name="filter_users")
]
