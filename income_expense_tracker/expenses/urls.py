from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

"""Url patterns for expenses view"""
urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('edit-expense/<int:id>', views.edit_expense, name='edit-expense'),
    path('delete-expense/<int:id>', views.delete_expense,
         name='delete-expense'),
    path('filter-expenses', csrf_exempt(views.filter_expenses),
         name='filter-expenses'),
]
