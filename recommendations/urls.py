from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_recommendations/', views.generate_recommendations, name='generate_recommendations'),
]
