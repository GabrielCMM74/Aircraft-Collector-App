from django.contrib import admin

# Register your models here.
from .models import Aircraft, Fueling

admin.site.register(Aircraft)
admin.site.register(Fueling)