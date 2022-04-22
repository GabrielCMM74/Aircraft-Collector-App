from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('aircrafts/', views.aircrafts_index, name='index'),
]