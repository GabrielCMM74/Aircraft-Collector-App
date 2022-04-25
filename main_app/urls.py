from django.urls import path

from .models import Aircraft
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('aircrafts/', views.aircrafts_index, name='index'),
    path('aircrafts/<int:aircraft_id>/', views.aircrafts_detail, name='detail'),
]