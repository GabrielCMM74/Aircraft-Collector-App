from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Aircraft, Service
from .forms import FuelingForm
# Add the following import
from django.http import HttpResponse


# class Aircraft:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, manufacturer, developedInto, description, dob, built):
#     self.name = name
#     self.manufacturer = manufacturer
#     self.description = description
#     self.developedInto = developedInto
#     self.dob = dob
#     self.built = built

# aircrafts = [
# Aircraft(
#     'F-16 Falcon',
#     'General Dynamics | Lockheed Martin', 
#     'General Dynamics F-16XL',
#     'The F-16 Fighting Falcon is a compact, multi-role fighter aircraft. It is highly maneuverable and has proven itself in air-to-air combat and air-to-surface attack.',
#     'January 20, 1974', 4604),

# Aircraft(
#     'Lockheed Martin F-22 Raptor',
#     'Lockheed Martin Aeuronautics | Boeing Defense | Space & Security', 
#     'Lockheed Martin X-44 MANTA',
#     'The aircraft is equipped to operate autonomously in combat over hostile territory, in escort of deep-penetration strike aircraft and in the suppression of enemy airfields. ',
#     'September 7, 1997', 195),
    
# Aircraft(
#     'Sukhoi Su-27',
#     'Sukhoi',
#     'Sukhoi Su-30', 
#     'The F-16 Fighting Falcon is a compact, multi-role fighter aircraft. It is highly maneuverable and has proven itself in air-to-air combat and air-to-surface attack.',
#     'May 20, 1977', 809),

# Aircraft(
#     'Grumman F-14 Tomcat',
#     'Grumman', 
#     'F-14D',
#     'The F-14D(R) Tomcat is a supersonic, twin-engine, variable sweep-wing, two-place strike fighter manufactured by Grumman Aircraft Corporation.',
#     'December 21, 1970', 712),
# ]
# Define the home view
def home(request):
    return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

def about(request):
    return render(request, 'about.html')

def aircrafts_index(request):
    aircrafts = Aircraft.objects.all()
    return render(request, 'aircrafts/index.html', { 'aircrafts': aircrafts })

def aircrafts_detail(request, aircraft_id):
    aircraft = Aircraft.objects.get(id=aircraft_id)
    fueling_form = FuelingForm
    return render(request, 'aircrafts/detail.html', { 'aircraft': aircraft, 'fueling_form': fueling_form })
# Create your views here.
class AircraftCreate(CreateView):
    model = Aircraft
    fields = '__all__'
    success_url = '/aircrafts/'

class AircraftUpdate(UpdateView):
    model = Aircraft
  # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['manufacturer', 'description', 'developedInto', 'built']

class AircraftDelete(DeleteView):
    model = Aircraft
    success_url = '/aircrafts/'

def add_fueling(request, aircraft_id):
    form = FuelingForm(request.POST)

    if form.is_valid():
        new_fueling = form.save(commit=False)
        new_fueling.aircraft_id = aircraft_id
        new_fueling.save()
    return redirect('detail', aircraft_id=aircraft_id)


class ServiceList(ListView):
  model = Service

class ServiceDetail(DetailView):
  model = Service

class ServiceCreate(CreateView):
  model = Service
  fields = '__all__'

class ServiceUpdate(UpdateView):
  model = Service
  fields = ['name', 'color']

class ServiceDelete(DeleteView):
  model = Service
  success_url = '/services/'










