from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from locations.models import Building, Room


# Create your models here.


class PhoneNumber(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='phones')
    number = PhoneNumberField(unique=True)

    def __str__(self):
        return f"{self.room.__str__()}: {self.number}"


class WorkingGroup(models.Model):
    name = models.CharField(max_length=50)
    department = models.CharField(blank=True, max_length=200)
    institution = models.CharField(blank=True, max_length=200)
    address = models.ManyToManyField(Building, blank=True)

    def __str__(self):
        return f"{self.name} group"


# todo: rename to member
class User(AbstractUser):
    # academic title (legal/ordering)
    working_group = models.ForeignKey(WorkingGroup, null=True, on_delete=models.PROTECT, related_name='members')
    phones = models.ManyToManyField(PhoneNumber, blank=True, related_name='contacts')
    rooms = models.ManyToManyField(Room, blank=True, related_name='team')
    # # identifiers, links (ORCID, ResearchGate, etc.)

    def __str__(self):
        return self.username
