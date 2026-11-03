from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField


class Building(models.Model):
    name = models.CharField(unique=True, max_length=50)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    state = models.CharField(blank=True, max_length=60)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='Germany')

    def __str__(self):
        return self.name


class Room(models.Model):
    # not the primary key: room numbers repeat across buildings
    number = models.IntegerField()
    floor = models.IntegerField(blank=True, null=True)
    # PROTECT: deleting a building must not silently delete its rooms
    building = models.ForeignKey(Building, blank=True, null=True, on_delete=models.PROTECT, related_name='rooms')
    type = models.TextField(
        blank=True,
        choices=[
            ('office', 'office'),
            ('lab', 'laboratory'),
            ('lec', 'lecture hall'),
            ('sem', 'seminar room'),
            ('none', 'other'),
        ]
    )

    def __str__(self):
        if self.type:
            return f"R{self.number} ({self.type})"
        return f"R{self.number}"

    class Meta:
        constraints = [
            # NULLS NOT DISTINCT (PostgreSQL 15+): one room 101 per building, also among rooms without a building
            models.UniqueConstraint(fields=['building', 'number'], name='room_unique_number_per_building', nulls_distinct=False),
        ]


class PhoneNumber(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='phones')
    number = models.CharField(max_length=20, unique=True)  # PhoneNumberField(unique=True)

    def __str__(self):
        return f"{self.room.__str__()}: {self.number}"


class Storage(models.Model):
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL, related_name="locations")
    name = models.CharField(max_length=50)
    compartment = models.CharField(blank=True, max_length=50)

    def __str__(self):
        prefix = f"R{self.room.number}: " if self.room else ""
        if self.compartment:
            return f"{prefix}{self.name} ({self.compartment})"
        return f"{prefix}{self.name}"

    class Meta:
        constraints = [
            # NULLS NOT DISTINCT: a storage without a room must not be duplicated either
            models.UniqueConstraint(fields=['room', 'name', 'compartment'], name='storage_unique_per_room', nulls_distinct=False),
        ]

    # todo: warnings for congregated storing of multiple compounds(containers)
