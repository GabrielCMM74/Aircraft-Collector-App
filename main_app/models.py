from datetime import date
from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
FUELTIMES = (
    ('B', 'Beginning of Flight'),
    ('M', 'Middle of Flight'),
    ('E', 'End of Flight')
)


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=50)
    priority = models.CharField(max_length=30)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services_detail', kwargs={'pk': self.id})




class Aircraft(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    developedInto = models.CharField(max_length=50)
    dob = models.CharField(max_length=50)
    built = models.IntegerField()
    services = models.ManyToManyField(Service)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # new code below
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'aircraft_id': self.id})

    def fueled_for_today(self):
        return self.fueling_set.filter(date=date.today()).count() >= len(FUELTIMES)

class Fueling(models.Model):
    date = models.DateField('Fueling Date')
    fuel = models.CharField(
        max_length=1,
        choices=FUELTIMES,
        default=FUELTIMES[0][0],
        )
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.get_fuel_display()} on {self.date}"
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for aircraft_id: {self.aircraft_id} @{self.url}"
# a = Aircraft(name="Lockheed Martin F-22 Raptor", manufacturer="Lockheed Martin Aeuronautics | Boeing Defense | Space & Security", description="The aircraft is equipped to operate autonomously in combat over hostile territory, in escort of deep-penetration strike aircraft and in the suppression of enemy airfields.", developedInto="Lockheed Martin X-44 MANTA", dob="September 7, 1997", built=195)
