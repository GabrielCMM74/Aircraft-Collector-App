from django.contrib import admin

# Register your models here.
from .models import Aircraft, Fueling, Service, Photo

admin.site.register(Aircraft)
admin.site.register(Fueling)
admin.site.register(Service)
admin.site.register(Photo)