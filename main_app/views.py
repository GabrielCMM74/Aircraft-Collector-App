from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Aircraft, Service
from .forms import FuelingForm

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'aircraftcollec'

import uuid
import boto3
from .models import Aircraft, Service, Photo
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

def about(request):
    return render(request, 'about.html')

@login_required
def aircrafts_index(request):
    aircrafts = Aircraft.objects.filter(user=request.user)
    return render(request, 'aircrafts/index.html', { 'aircrafts': aircrafts })

@login_required
def aircrafts_detail(request, aircraft_id):
    aircraft = Aircraft.objects.get(id=aircraft_id)
    services_aircraft_doesnt_have = Service.objects.exclude(id__in = aircraft.services.all().values_list('id'))
    fueling_form = FuelingForm
    return render(request, 'aircrafts/detail.html', { 'aircraft': aircraft, 'fueling_form': fueling_form, 'services' : services_aircraft_doesnt_have })

class AircraftCreate(LoginRequiredMixin, CreateView):
    model = Aircraft
    fields = ['name','manufacturer', 'description', 'developedInto', 'dob', 'built']
    success_url = '/aircrafts/'

    def form_valid(self, form):
      form.instance.user = self.request.user  
      return super().form_valid(form)

class AircraftUpdate(UpdateView):
    model = Aircraft
    fields = ['manufacturer', 'description', 'developedInto', 'built']

class AircraftDelete(LoginRequiredMixin, DeleteView):
    model = Aircraft
    success_url = '/aircrafts/'

@login_required
def add_fueling(request, aircraft_id):
    form = FuelingForm(request.POST)

    if form.is_valid():
        new_fueling = form.save(commit=False)
        new_fueling.aircraft_id = aircraft_id
        new_fueling.save()
    return redirect('detail', aircraft_id=aircraft_id)


class ServiceList(LoginRequiredMixin, ListView):
  model = Service

class ServiceDetail(LoginRequiredMixin, DetailView):
  model = Service

class ServiceCreate(LoginRequiredMixin, CreateView):
  model = Service
  fields = '__all__'

class ServiceUpdate(LoginRequiredMixin, UpdateView):
  model = Service
  fields = ['name', 'color']

class ServiceDelete(LoginRequiredMixin, DeleteView):
  model = Service
  success_url = '/services/'

@login_required
def assoc_service(request, aircraft_id, service_id):
    Aircraft.objects.get(id=aircraft_id).services.add(service_id)
    return redirect('detail', aircraft_id=aircraft_id)

@login_required
def unassoc_service(request, aircraft_id, service_id):
    Aircraft.objects.get(id=aircraft_id).services.remove(service_id)
    return redirect('detail', aircraft_id=aircraft_id)

@login_required
def add_photo(request, aircraft_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            Photo.objects.create(url=url, aircraft_id=aircraft_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', aircraft_id=aircraft_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)







