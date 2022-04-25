from django.forms import ModelForm
from .models import Fueling

class FuelingForm(ModelForm):
  class Meta:
    model = Fueling
    fields = ['date', 'fuel']