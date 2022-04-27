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


# Add the following import
import uuid
import boto3
from .models import Aircraft, Service, Photo
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
# Create your views here.
class AircraftCreate(LoginRequiredMixin, CreateView):
    model = Aircraft
    fields = ['name','manufacturer', 'description', 'developedInto', 'dob', 'built']
    success_url = '/aircrafts/'

    def form_valid(self, form):
    # Assign the logged in user (self.request.user)
      form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
      return super().form_valid(form)

class AircraftUpdate(UpdateView):
    model = Aircraft
  # Let's disallow the renaming of a cat by excluding the name field!
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
  # Note that you can pass a toy's id instead of the whole object
    Aircraft.objects.get(id=aircraft_id).services.add(service_id)
    return redirect('detail', aircraft_id=aircraft_id)

@login_required
def unassoc_service(request, aircraft_id, service_id):
  # Note that you can pass a toy's id instead of the whole object
    Aircraft.objects.get(id=aircraft_id).services.remove(service_id)
    return redirect('detail', aircraft_id=aircraft_id)

@login_required
def add_photo(request, aircraft_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, aircraft_id=aircraft_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', aircraft_id=aircraft_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)







