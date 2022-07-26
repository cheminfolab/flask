from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from .fields import BarcodeField

from accounts.models import WorkingGroup, Member
from locations.models import Storage
from ghs.models import GHS

# MISCELLANEOUS

si_units = []


class Prefix(models.Model):
    name = models.CharField(blank=True, max_length=10)
    symbol = models.CharField(max_length=2, unique=True)
    factor = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.symbol}): {self.factor:.0E}"

    class Meta:
        verbose_name_plural = 'prefixes'


class SI(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    def is_valid(self):
        return self.symbol in si_units

    class Meta:
        verbose_name_plural = 'SI'


class Unit(models.Model):
    name = models.CharField(max_length=50)
    prefix = models.ForeignKey(
        Prefix, blank=True, null=True, on_delete=models.PROTECT, related_name='unit_prefixes'
    )
    symbol = models.CharField(max_length=10)
    si = models.ManyToManyField(
        SI, blank=True, related_name='units', through='DerivedUnit'
    )
    factor = models.FloatField(default=1)
    type = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = (('prefix', 'symbol'),)


class DerivedUnit(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    si = models.ForeignKey(SI, on_delete=models.PROTECT)
    exponent = models.IntegerField(default=1)
    factor = models.FloatField(default=1)

    def __str__(self):
        if self.exponent == 1:
            return f"{self.unit.symbol}: {self.factor} {self.si.symbol}"
        return f"{self.unit.symbol}: {self.factor} {self.si.symbol}^{self.exponent}"


class Currency(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Currencies'


class Category(models.Model):
    name = models.CharField(max_length=100)

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

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/substances/<filename>
    return 'substances/{0}'.format(filename)


class Substance(models.Model):
    # import uuid
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    names = ArrayField(models.CharField(blank=True, max_length=250), default=list)
    # most common name (trivial name)?

    formula = models.CharField(blank=True, max_length=100)  # JSONField()
    # todo: add validators (Hill notation)

    # structural identifiers
    smiles = models.CharField(blank=True, max_length=100)
    inchi = models.CharField(blank=True, max_length=100)
    inchi_key = models.CharField(blank=True, max_length=100)
    # mdl
    # STEREOCHEMISTRY?? enantiomers, distereomers, racemic mixtures?
    molecule = models.CharField(blank=True, max_length=250)  # rd_models.MolField()  #
    # mol file (type: crystal structure, calculated (conditions))
    # cif: crystal structure

    # other identifiers
    cas = models.CharField(blank=True, max_length=12)  # todo: add validator
    pubchem_sid = models.IntegerField(blank=True, null=True)
    # 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/<cid>/property/MolecularFormula,MolecularWeight/CSV'
    # 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/<cid>/JSON'
    # ec number (european community), german: EG
    # https://echa.europa.eu/information-on-chemicals/ec-inventory

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
    # decomposition temperature
    # auto-ignition temp.
    # viscosity
    # refractive index

    # vapor density
    # vapor pressure
    # solubility
    # logP
    # stability (shelf life)
    # todo: properties as array? (substance vs compound?)

    image = models.ImageField(blank=True, null=True, upload_to=user_directory_path)

    # mol file ? (params: 2D/3D optimized, etc.)
    # ccsd ?
    # torsionbv = models.BfpField(null=True)
    # mfp2 = models.BfpField(null=True)
    # ffp2 = models.BfpField(null=True)

    # wikipedia, CPDat, ChEMBL, ChemSpider, CHEMnetBASE, GESTIS(SDS), NFDI, SpectraBASE (slugfields?), Massbank!

    def __str__(self):
        return self.names[0]


class Compound(models.Model):
    substance = models.ForeignKey(
        Substance, null=True, on_delete=models.PROTECT, related_name="compounds"
    )
    # todo: mixtures? (diluted substances, etc.)
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

    # # todo: change to many-to-one relation
    # container = models.OneToOneField(
    #     Container, null=True, on_delete=models.CASCADE, related_name='containing_compounds'
    # )

    purity = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], default=100
    )
    density = models.FloatField(null=True, blank=True)  # todo: move to substance?
    #                                                   #  what about mixtures??
    density_unit = models.ForeignKey(
        Unit, blank=True, null=True, on_delete=models.PROTECT, related_name="density_units"
    )

    ghs = models.OneToOneField(
        GHS, null=True, on_delete=models.PROTECT, related_name='hazardous_compounds'
    )
    # sds
    # un number (adr, adn, ADNR und ADN-D, RID, SOLAS)

    # Lagerklassen
    # Arbeitsplatzgrenzwerte(AGW)
    # Biologische
    # Arbeitsplatztoleranzwerte(BAT)
    # Wassergefährdungsklassen
    # Global Warming Potential(des ICC)

    # classification
    #
    # EC-Nummern (REACH)
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

    # spectra

    category = models.ManyToManyField(Category, blank=True, related_name='categorized_compounds')

    # related compounds (hydrates, hydrochlorides, etc.)

    # spectra

    created_by = models.ForeignKey(
        Member, null=True, on_delete=models.SET_NULL, related_name='created_compounds'  # default ??
    )
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.substance.names[0]}"


class Container(models.Model):
    compound = models.ForeignKey(
        Compound, null=True, on_delete=models.PROTECT, related_name="containers"
    )
    supplier = models.CharField(max_length=250)
    EAN = BarcodeField(blank=True)
    product_number = models.CharField(blank=True, max_length=100)
    # batch_number (self-made: auto-generate?)
    # sku (stock-keeping unit)
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
    owner = models.ForeignKey(
        WorkingGroup, blank=True, null=True, on_delete=models.PROTECT, related_name="group_chemicals"
    )

    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    currency = models.ForeignKey(
        Currency, blank=True, null=True, on_delete=models.PROTECT, related_name="currencies"
    )

    description = models.CharField(blank=True, max_length=500)

    conditions = models.CharField(blank=True, max_length=50)  # argon, molecular sieve etc. (checkboxes?)

    opened = models.DateField(blank=True, null=True)
    last_used = models.DateField(blank=True, null=True)
    last_user = models.OneToOneField(
        Member, blank=True, null=True, on_delete=models.SET_NULL, related_name='last_compounds'
    )

    # spectra
    # inspection cycle

    # todo: solve refilling from other container (e.g. after destillation)?

    def __str__(self):
        return f"{self.compound.substance.names[0]} ({self.supplier})"
