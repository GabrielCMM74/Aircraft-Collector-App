from django.urls import path

from .models import Aircraft
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('aircrafts/', views.aircrafts_index, name='index'),
    path('aircrafts/<int:aircraft_id>/', views.aircrafts_detail, name='detail'),
    path('aircrafts/create/', views.AircraftCreate.as_view(), name='aircrafts_create'),
    path('aircrafts/<int:pk>/update/', views.AircraftUpdate.as_view(), name='aircrafts_update'),
    path('aircrafts/<int:pk>/delete/', views.AircraftDelete.as_view(), name='aircrafts_delete'),
]