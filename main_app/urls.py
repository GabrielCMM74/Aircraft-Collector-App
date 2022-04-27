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
    path('aircrafts/<int:aircraft_id>/add_fueling/', views.add_fueling, name='add_fueling'),
    path('aircrafts/<int:aircraft_id>/assoc_service/<int:service_id>/', views.assoc_service, name='assoc_service'),
    path('aircrafts/<int:aircraft_id>/unassoc_service/<int:service_id>/', views.unassoc_service, name='unassoc_service'),
    path('aircrafts/<int:aircraft_id>/add_photo/', views.add_photo, name='add_photo'),
    path('services/', views.ServiceList.as_view(), name='services_index'),
    path('services/<int:pk>/', views.ServiceDetail.as_view(), name='services_detail'),
    path('services/create/', views.ServiceCreate.as_view(), name='services_create'),
    path('services/<int:pk>/update/', views.ServiceUpdate.as_view(), name='services_update'),
    path('services/<int:pk>/delete/', views.ServiceDelete.as_view(), name='services_delete'),
    path('accounts/signup/', views.signup, name='signup'),

]