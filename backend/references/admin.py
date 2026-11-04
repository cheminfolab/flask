from django.contrib import admin
from .models import *

admin.site.register(Organization)
admin.site.register(Author)
admin.site.register(CoAuthor)
admin.site.register(Journal)
admin.site.register(Reference)