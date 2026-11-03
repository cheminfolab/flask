from django.db import models

from api.models import Tag


class Organization(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class CoAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    order = models.IntegerField(blank=False)
    corresponding = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} ({self.order})"


class Journal(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.name


class Reference(models.Model):
    citation_key = models.CharField(unique=True, blank=False, max_length=50)
    type = models.CharField(
        max_length=20,
        choices=[
            ("article", "journal article"),
            ("book", "book"),
            ("collection", "collection"),
            ("manual", "manual"),
            ("misc", "miscellaneous"),
            ("online", "website"),
            ("patent", "patent"),
            ("proceedings", "proceedings"),
            ("report", "report"),
            ("thesis", "thesis"),
            ("unpublished", "unpublished"),
        ],
        default="article",
    )
    title = models.CharField(blank=True, max_length=200)
    journal = models.ForeignKey(Journal, blank=True, null=True, on_delete=models.PROTECT, related_name="journals")
    abstract = models.CharField(blank=True, max_length=500)
    authors = models.ManyToManyField(CoAuthor, related_name="authors")
    editors = models.ManyToManyField(CoAuthor, related_name="editors")
    location = models.CharField(blank=True, max_length=50)
    publisher = models.CharField(blank=True, max_length=50)
    # organization = models.ManyToManyField(Organization, related_name="organizations")
    # institution = models.CharField(blank=True, max_length=50)
    date = models.DateField(blank=True)
    series = models.IntegerField(blank=True, null=True)
    chapter = models.IntegerField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    part = models.IntegerField(blank=True, null=True)
    number = models.CharField(blank=True, max_length=50)
    edition = models.CharField(blank=True, max_length=50)
    pages = models.CharField(blank=True, max_length=50)
    version = models.IntegerField(blank=True, null=True)
    doi = models.CharField(blank=True, max_length=50)
    isbn = models.CharField(blank=True, max_length=50)
    url = models.URLField(blank=True)
    keywords = models.ManyToManyField(Tag, related_name="keywords")
    # citations = models.ManyToManyField("self", related_name="references")
    # cited_by = models.ManyToManyField("self", related_name="cited by")
    retracted = models.BooleanField(default=False)
    expired = models.BooleanField(blank=True, null=True)