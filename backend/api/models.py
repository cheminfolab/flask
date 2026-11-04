from django.conf import settings
from django.db import models


class TrackedModel(models.Model):
    """
    Provenance fields for records whose authorship matters.

    `created_by` / `updated_by` are assigned by the API (see
    api.views.BaseModelViewSet), never taken from the client. Users are
    protected from deletion while they authored records: deactivate them instead.
    Change history (previous values, who, when) is kept separately by
    django-simple-history (`history = HistoricalRecords()` on concrete models).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, editable=False,
        on_delete=models.PROTECT, related_name='+',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, editable=False,
        on_delete=models.PROTECT, related_name='+',
    )

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(max_length=100)
    # TODO: validate strict hierarchy
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Abbreviation(models.Model):
    short = models.CharField(max_length=50)
    long = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.long} ({self.short})"