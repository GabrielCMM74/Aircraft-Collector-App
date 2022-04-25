from sys import builtin_module_names, dont_write_bytecode
from django.db import models

# Create your models here.
class Aircraft(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    developedInto = models.TextField(max_length=50)
    dob = models.TextField(max_length=50)
    built = models.IntegerField()
    # new code below
    def __str__(self):
        return self.name




# a = Aircraft(name="Lockheed Martin F-22 Raptor", manufacturer="Lockheed Martin Aeuronautics | Boeing Defense | Space & Security", description="The aircraft is equipped to operate autonomously in combat over hostile territory, in escort of deep-penetration strike aircraft and in the suppression of enemy airfields.", developedInto="Lockheed Martin X-44 MANTA", dob="September 7, 1997", built=195)
