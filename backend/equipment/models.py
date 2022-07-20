from django.db import models
from locations.models import Room


# Create your models here.

class Computer(models.Model):
    room = models.ForeignKey(Room, null=True, on_delete=models.PROTECT, related_name='computers')
    name = models.CharField(blank=True, max_length=50)
    static_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name


class Spectrometer(models.Model):
    type = models.CharField(
        max_length=10,
        choices=[('nmr', 'NMR'), ('ms', 'MS'), ('gc', 'GC'), ('gcms', 'GC-MS'), ('lcms', 'LC-MS'), ('hplc', 'HPLC')])
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    annotation = models.TextField(blank=True)
