from django.contrib import admin
from .models import *


# Register your models here.

class ContainerAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'amount', 'amount_left', 'amount_unit', 'description')


class CompoundAdmin(admin.ModelAdmin):
    # inlines = []
    list_display = ('substance', 'container', 'annotation')
    # ('substance.formula', 'substance.mol_weight', 'substance.trivial_name', 'producer', 'location')


class CompoundInline(admin.TabularInline):
    model = Compound
    extra = 0


class SubstanceAdmin(admin.ModelAdmin):
    inlines = [
        CompoundInline
    ]
    list_display = ('names', 'molecule')  # ('formula', 'mol_weight', 'trivial_name')


admin.site.register(Unit)
admin.site.register(Currency)

admin.site.register(Container)
admin.site.register(Substance, SubstanceAdmin)
admin.site.register(Compound, CompoundAdmin)
