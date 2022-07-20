from django.db import models


# Create your models here.
class Building(models.Model):
    name = models.CharField(unique=True, max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    state = models.CharField(blank=True, max_length=60)
    zipcode = models.CharField(max_length=5)
    country = models.CharField(max_length=50, default='Germany')

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.IntegerField(primary_key=True)
    floor = models.IntegerField(blank=True, null=True)
    building = models.ForeignKey(Building, blank=True, null=True, on_delete=models.CASCADE, related_name='rooms')
    type = models.TextField(
        blank=True,
        choices=[('office', 'office'), ('lab', 'laboratory'), ('lec', 'lecture hall'), ('sem', 'seminar room')]
    )

    def __str__(self):
        if self.type:
            return f"R{self.number} ({self.type})"
        return f"R{self.number}"

    class Meta:
        unique_together = (('number', 'floor', 'building'),)


class Storage(models.Model):
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL, related_name="locations")
    name = models.CharField(max_length=50)
    compartment = models.CharField(blank=True, max_length=50)

    def __str__(self):
        if self.compartment:
            return f"R{self.room.number}: {self.name} ({self.compartment})"
        return f"R{self.room.number}: {self.name}"

    class Meta:
        unique_together = (('room', 'name', 'compartment'),)

    # todo: warnings for congregated storing of multiple compounds(containers)

