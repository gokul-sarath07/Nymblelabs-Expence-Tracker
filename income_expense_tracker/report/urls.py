from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.stats_view, name="stats"),
    path('category-summery', views.category_summery, name="category-summery"),
    path('weekly-summery', views.weekly_summery, name="weekly-summery"),
]
