from django.db import models
# from django_rdkit import models as rk_models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

from barcode_field.fields import BarcodeField

from accounts.models import WorkingGroup, Member, Supplier
from locations.models import Storage
from ghs.models import GHS


class Prefix(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name}"


class Unit(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Currency(models.Model):
    name = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name_plural = 'Currencies'


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

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


# CHEMICALS

def substance_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/substances/<filename>
    return f'substances/{filename}'


#####################################################################################


class UnitCell(models.Model):
    a = models.FloatField(null=True)
    b = models.FloatField(null=True)
    c = models.FloatField(null=True)
    alpha = models.FloatField(null=True)
    beta = models.FloatField(null=True)
    gamma = models.FloatField(null=True)


class Structure(models.Model):
    # COORDINATES
    atoms = ArrayField(
        models.CharField(blank=True, max_length=3),
        blank=True,
        default=list
    )
    # indexes ?
    coordinates = ArrayField(
        ArrayField(
            models.FloatField(blank=True, null=True),
            blank=True,
            default=list
        ),
        blank=True,
        size=3,
        default=list
    )
    bonds = ArrayField(
        ArrayField(
            models.IntegerField(blank=True, null=True),
            size=2,
            default=list
        ),
        blank=True,
        default=list
    )
    labels = ArrayField(
        models.CharField(blank=True, max_length=3),
        blank=True,
        default=list
    )
    unitcell = models.OneToOneField(UnitCell, on_delete=models.SET_NULL, blank=True, null=True)

    # CALCULATION CONDITIONS
    # basis set (as separate model? fetch from basissetexchange?)
    # orbitals (how to represent?)

    type = models.CharField(blank=True, max_length=50)  # todo: CHOICES (calculation / crystal structure / ...)
    description = models.TextField(blank=True)  # (measurement) conditions

    # FILES
    # cif, mol, ...
    # rdkit = rk_models.MolField(blank=True, null=True)

    # FINGERPRINTS / FRAGMENTS
    # torsionbv = models.BfpField(null=True)
    # mfp2 = models.BfpField(null=True)
    # ffp2 = models.BfpField(null=True)


class Substance(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)  # IUPAC
    synonyms = ArrayField(
        models.CharField(blank=True, max_length=250),
        blank=True,
        default=list
    )
    label = models.CharField(blank=True, max_length=250)  # trivial name
    formula = models.CharField(blank=True, max_length=100)  # todo: add validators (Hill notation)

    # IDENTIFIERS
    smiles = models.CharField(blank=True, max_length=100)
    # smarts
    inchi = models.CharField(blank=True, max_length=100)
    inchi_key = models.CharField(blank=True, max_length=100)
    # todo: add validators

    cas = models.CharField(blank=True, max_length=12)  # todo: add validator
    pubchem_sid = models.IntegerField(blank=True, null=True)
    pubchem_cid = models.IntegerField(blank=True, null=True)

    # STRUCTURE
    structure = models.ManyToManyField(Structure, blank=True, related_name='substance_structures')
    # STEREOCHEMISTRY?? enantiomers, distereomers, racemic mixtures?

    # PROPERTIES
    mol_weight = models.FloatField(blank=True, null=True)
    mol_weight_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="mol_weight_units"
    )
    exact_mass = models.FloatField(blank=True, null=True)
    exact_mass_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="exact_mass_units"
    )

    image = models.ImageField(blank=True, null=True, upload_to=substance_directory_path)

    def __str__(self):
        if self.label:
            return self.label
        return self.name


class Component(models.Model):
    substance = models.ForeignKey(Substance, on_delete=models.PROTECT, related_name='components')
    fraction = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.00)], default=1.00
    )
    type = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return f"{self.substance.name} ({self.fraction*100}%)"


class Compound(models.Model):
    name = models.CharField(max_length=250)  # IUPAC
    synonyms = ArrayField(
        models.CharField(blank=True, max_length=250),
        blank=True,
        default=list
    )
    label = models.CharField(blank=True, max_length=250)
    substances = models.ManyToManyField(Component, blank=False, related_name='compounds')
    purity = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.00)], default=1.00
    )

    # PROPERTIES
    density = models.FloatField(null=True, blank=True)
    density_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="density_units"
    )
    # physical state at normal conditions (gaseous, liquid, solid, hypercritical,...)
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
    # decomposition temperature
    # auto-ignition temp.
    # viscosity
    # refractive index
    # vapor density
    # vapor pressure
    # solubility (solvent???)
    # logP
    # stability (shelf life)
    # todo: properties as array? (substance vs compound?)

    # SAFETY
    ghs = models.OneToOneField(
        GHS, blank=True, null=True, on_delete=models.PROTECT, related_name='hazardous_compounds'
    )
    # SDS (pdf)
    # UN number (adr, adn, ADNR und ADN-D, RID, SOLAS)
    # Lagerklassen
    # Arbeitsplatzgrenzwerte(AGW)
    # Biologische
    # Arbeitsplatztoleranzwerte(BAT)
    # Wassergefährdungsklassen
    # Global Warming Potential(des ICC)

    # CLASSIFICATION
    #
    # EC-Nummern (REACH)    # ec number (european community), german: EG
    # https://echa.europa.eu/information-on-chemicals/ec-inventory
    # UN-Nr. (ADR)
    # Zoll-Nummern
    # Dual-Use Kategorie
    # Colour-Index
    # BtMG
    # CWÜ- und BWÜ-Listen
    # Doping (WADA-Liste)
    # ATC-Codes
    # EINECS / ELINCS / NLP
    # Stoffgruppe Sprengstoff-Gesetz
    # Ausführliche Regelungen für die Schule (SR-2004)
    # Einstufung als Biologischer Arbeitsstoff
    # Gruppe in der Seveso III-Verordnung

    categories = models.ManyToManyField(Category, blank=True, related_name='categorized_compounds')
    # related compounds (hydrates, hydrochlorides, etc.), see also fingeprints

    # spectra

    created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        Member, null=True, on_delete=models.SET_NULL, related_name='compounds_created'
    )

    def __str__(self):
        if self.label:
            return f"{self.label} {self.purity*100}%"
        return f"{self.name} {self.purity*100}%"


class Container(models.Model):
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, related_name="children"
    )
    compound = models.ForeignKey(
        Compound, null=True, on_delete=models.PROTECT, related_name="containers"
    )
    tara = models.FloatField(blank=True, null=True)  # container weight including cap
    tara_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="tara_units"
    )
    amount = models.FloatField(null=True)
    amount_left = models.FloatField(blank=True, null=True)
    amount_unit = models.ForeignKey(
        Unit, null=True, on_delete=models.PROTECT, related_name="amount_units"
    )
    # is_active (False, when amount_left = 0)

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="products")
    EAN = BarcodeField(blank=True)
    product_number = models.CharField(blank=True, max_length=100)
    # batch_number (self-made: auto-generate?)
    # sku (stock-keeping unit)

    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    currency = models.ForeignKey(
        Currency, blank=True, null=True, on_delete=models.PROTECT, related_name="currencies"
    )
    location = models.ForeignKey(
        Storage, null=True, on_delete=models.SET_NULL, related_name="containments"
    )
    owner = models.ForeignKey(
        WorkingGroup, blank=True, null=True, on_delete=models.PROTECT, related_name="group_chemicals"
    )

    description = models.CharField(blank=True, max_length=500)

    conditions = models.CharField(blank=True, max_length=50)  # argon, molecular sieve etc. (checkboxes?)

    created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        Member, null=True, on_delete=models.SET_NULL, related_name='containers_created'
    )
    opened = models.DateField(blank=True, null=True)
    last_used = models.DateField(blank=True, null=True)
    last_user = models.OneToOneField(
        Member, blank=True, null=True, on_delete=models.SET_NULL, related_name='compounds_used_last'
    )
    # future user ??

    # spectra
    # inspection cycle

    def __str__(self):
        return f"{self.compound.__str__()} ({self.supplier})"


# DATABASES
# PUGView
# PUGREST
# wikipedia
# CPDat
# ChEMBL
# ChemSpider
# CHEMnetBASE
# GESTIS(SDS)
# NFDI
# SpectraBASE (slugfields?),
# Massbank
# CCSD
# (retractionwatch)
