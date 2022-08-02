from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from .fields import BarcodeField

from accounts.models import WorkingGroup, Member
from locations.models import Storage


# MISCELLANEOUS

class Unit(models.Model):
    prefix = models.CharField(
        max_length=10,
        choices=[('m', 'milli'), ('c', 'centi'), ('d', 'deci'), ('h', 'hecto'), ('k', 'kilo')],
        blank=True
    )
    si = models.CharField(
        max_length=10,
        choices=[
            ('g', 'gram'), ('l', 'liter'), ('g/mol', 'gram per mol'), ('g/ml', 'gram per milliliter')
        ]
    )
    # todo: change to lower case?
    type = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return f"{self.prefix}{self.si}"

    class Meta:
        unique_together = (('prefix', 'si'),)


class Currency(models.Model):
    currency = models.CharField(max_length=10, choices=[('EUR', 'euro'), ('USD', 'us dollar')], unique=True)
    # todo: change to name!

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name_plural = 'Currencies'


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/substances/<filename>
    return 'substances/{0}'.format(filename)


class Container(models.Model):
    supplier = models.CharField(max_length=250)
    EAN = BarcodeField(blank=True)
    product_number = models.CharField(blank=True, max_length=100)
    # batch_number (self-made: auto-generate?)
    amount = models.FloatField(null=True)
    amount_left = models.FloatField(blank=True, null=True)
    amount_unit = models.ForeignKey(
        Unit, null=True, on_delete=models.PROTECT, related_name="amount_units"
    )
    # is_active (False, when amount_left = 0)
    tara = models.FloatField(blank=True, null=True)  # container weight including cap
    tara_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="tara_units"
    )
    location = models.ForeignKey(
        Storage, null=True, on_delete=models.SET_NULL, related_name="containments"
    )
    # storing conditions: argon, molecular sieve etc. (checkboxes?)
    description = models.CharField(blank=True, max_length=50)

    # inspection cycle

    # todo: solve refilling from other container (e.g. after destillation)?


# CHEMICALS

class Substance(models.Model):
    # import uuid
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    names = ArrayField(models.CharField(blank=True, max_length=250), default=list)
    # most common name (trivial name)?

    molecule = models.CharField(blank=True, max_length=250)  # rd_models.MolField()  #
    formula = models.CharField(blank=True, max_length=100)  # JSONField()
    # todo: add validators

    # structural identifiers
    smiles = models.CharField(blank=True, max_length=100)
    inchi = models.CharField(blank=True, max_length=100)
    inchi_key = models.CharField(blank=True, max_length=100)
    # STEREOCHEMISTRY??

    # other identifiers
    cas = models.CharField(blank=True, max_length=12)  # todo: add validator
    pubchem_sid = models.IntegerField(blank=True, null=True)
    # 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/<cid>/property/MolecularFormula,MolecularWeight/CSV'
    # 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/<cid>/JSON'

    # properties
    mol_weight = models.FloatField(blank=True, null=True)
    mol_weight_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="mol_weight_units"
    )
    exact_mass = models.FloatField(blank=True, null=True)
    exact_mass_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="exact_mass_units"
    )
    # physical state (gaseous, liquid, solid, hypercritical,...)
    color = models.CharField(blank=True, max_length=20)
    melting_point = models.FloatField(blank=True, null=True)
    melting_point_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="melting_point_units"
    )
    boiling_point = models.FloatField(blank=True, null=True)
    boiling_point_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="boiling_point_units"
    )
    flash_point = models.FloatField(blank=True, null=True)
    flash_point_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="flash_point_units"
    )
    # vapor density
    # vapor pressure
    # solubility
    # logP
    # auto-ignition temp.
    # stability (shelf life)
    # viscosity
    # refractive index

    image = models.ImageField(blank=True, null=True, upload_to=user_directory_path)

    # mol file ? (params: 2D/3D optimized, etc.)
    # ccsd ?
    # torsionbv = models.BfpField(null=True)
    # mfp2 = models.BfpField(null=True)
    # ffp2 = models.BfpField(null=True)

    # wikipedia, CPDat, ChEMBL, ChemSpider, CHEMnetBASE, GESTIS(SDS), NFDI, SpectraBASE (slugfields?), Massbank!
    
    # spectra

    def __str__(self):
        return self.names[0]


class Compound(models.Model):
    substance = models.ForeignKey(
        Substance, null=True, on_delete=models.PROTECT, related_name="compounds"
    )
    # what about mixtures (diluted substances, etc.)

    # mixtures:
    #
    # Petrolether 30-50 und Petrolether 50-70 mit und ohne Benzol
    # Salzsäure 10% und 37%-ig in Wasser oder in Methanol
    # Eisen als Block oder Pulver
    # Kieselgel, normal oder als Blau- oder Orangegel
    # Standardlösungen (AAS) und Pufferlösungen
    # Ionenaustauscher
    # Petrochemische Produkte und Lösungsmittel
    # Pflanzenextrakte
    # traditionelle Arzneistoffe

    pubchem_cid = models.IntegerField(blank=True, null=True)

    # classification
    #
    # Zoll-Nummern
    # CAS-Nummern
    # Dual-Use Kategorie
    # UN-Nr. (ADR)
    # Colour-Index
    # BtMG
    # CWÜ- und BWÜ-Listen
    # Doping (WADA-Liste)
    # ATC-Codes
    # EC-Nummern (REACH)
    # EINECS / ELINCS / NLP
    # Stoffgruppe Sprengstoff-Gesetz
    # Ausführliche Regelungen für die Schule (SR-2004)
    # Einstufung als Biologischer Arbeitsstoff
    # Gruppe in der Seveso III-Verordnung

    container = models.OneToOneField(
        Container, null=True, on_delete=models.CASCADE, related_name='containing_compounds'
    )

    purity = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], default=100
    )
    density = models.FloatField(null=True, blank=True)  # todo: move to substance?
    #                                                   #  what about mixtures??
    density_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="density_units"
    )
    opened = models.DateField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)  # normalize two decimals
    currency = models.ForeignKey(
        Currency, blank=True, null=True, on_delete=models.PROTECT, related_name="currencies"
    )
    owner = models.ForeignKey(
        WorkingGroup, blank=True, null=True, on_delete=models.PROTECT, related_name="group_chemicals"
    )
    annotation = models.CharField(blank=True, max_length=500)
    last_user = models.OneToOneField(
        Member, blank=True, null=True, on_delete=models.SET_NULL, related_name='last_compounds'
    )
    last_used = models.DateField(blank=True, null=True)

    # ghs
    # sds
    # un number (adr, adn, ADNR und ADN-D, RID, SOLAS)

    # hazards
    # Lagerklassen
    # Arbeitsplatzgrenzwerte(AGW)
    # Biologische
    # Arbeitsplatztoleranzwerte(BAT)
    # Wassergefährdungsklassen
    # Global
    # Warming
    # Potential(des ICC)

    # related compounds (hydrates, hydrochlorides, etc.)

    # compound class:
    #
    # Organika
    # Anorganika
    # Biozide & Pestizide
    # Arzneistoffe
    # Betäubungsmittel
    # Psychoaktive Stoffe
    # Lebensmittelzusatzstoffe
    # Futtermittel
    # Enzyme
    # Biologische Arbeitsstoffe
    # Mikroorganismen
    # Verbrauchsmaterialien & Trennmaterialien
    # Dual-Use-Stoffe
    # Biowaffen & Chemiewaffen
    # FCKW & Klimagase
    # Standard-Referenz-Materialien uva

    # spectra
    created_by = models.ForeignKey(
        Member, null=True, on_delete=models.SET_NULL, related_name='created_compounds'  # default ??
    )
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.substance.names[0]} ({self.container.supplier})"
