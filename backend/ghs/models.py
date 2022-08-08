from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator


class Pictogram(models.Model):
    description = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='')

    def __str__(self):
        return f"{self.description}"


class HazardClass(models.Model):
    code = models.CharField(max_length=2, validators=[MinLengthValidator(2)])  # subclasses? 2.1. explosive gases
    name = models.CharField(max_length=20)
    pictogram = models.ForeignKey(Pictogram, null=True, on_delete=models.PROTECT)
    # 1. explosives, 2. gases
    # subclasses?

    def __str__(self):
        return f"GHS{self.code}"

    class Meta:
        unique_together = (('code', 'name'),)
        verbose_name_plural = 'hazard classes'


class PrecautionaryStatement(models.Model):
    code = ArrayField(
        models.CharField(max_length=3, validators=[MinLengthValidator(3)]),
        unique=True,
        default=list
    )
    category = models.TextField(
        choices=(
            ('prevention', 'prevention'),
            ('response', 'response'),
            ('storage', 'storage'),
            ('disposal', 'disposal')
        )
    )
    statements = ArrayField(
        models.TextField(),
        default=list
    )

    def __str__(self):
        if len(self.code) > 1:
            return '+'.join(['P'+str(p) for p in self.code])
        return f"P{self.code[0]}"


class HazardStatement(models.Model):
    code = ArrayField(
        models.CharField(max_length=5, validators=[MinLengthValidator(3)]),
        unique=True,
        default=list
    )
    category = models.TextField(
        choices=(
            ('physical', 'physical'),
            ('health', 'health'),
            ('environmental', 'environmental'),
            ('disposal', 'disposal')
        )
    )
    statements = ArrayField(
        models.TextField(),
        default=list
    )

    # un_category = models.TextField()
    # un = models.TextField()
    signal_word = models.CharField(max_length=20, choices=(('danger', 'danger'), ('warning', 'warning')))

    def __str__(self):
        if len(self.code) > 1:
            return '+'.join(['H'+str(h) for h in self.code])
        return f"H{self.code[0]}"


class GHS(models.Model):
    hazard_classes = models.ManyToManyField(HazardClass)
    H = models.ManyToManyField(HazardStatement)
    P = models.ManyToManyField(PrecautionaryStatement)

    class Meta:
        verbose_name = 'GHS'
        verbose_name_plural = 'GHS'


# https://pubchem.ncbi.nlm.nih.gov/ghs/#_prec
