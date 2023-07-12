from django.contrib import admin
from .models import *


class DerivedUnitInline(admin.TabularInline):
    model = DerivedUnit
    extra = 0
    readonly_fields = ('factor', 'si', 'exponent')


class UnitAdmin(admin.ModelAdmin):
    inlines = [
        DerivedUnitInline
    ]
    # list_display = ('names', 'formula', 'mol_weight')


class ContainerAdmin(admin.ModelAdmin):
    list_display = ('compound', 'supplier', 'amount', 'amount_left', 'amount_unit', 'description')


class CompoundAdmin(admin.ModelAdmin):
    # inlines = []
    list_display = ('substance',)


class CompoundInline(admin.TabularInline):
    model = Compound
    extra = 0


class SubstanceAdmin(admin.ModelAdmin):
    inlines = [
        CompoundInline
    ]
    list_display = ('names', 'formula', 'mol_weight')


admin.site.register(Prefix)
admin.site.register(SI)
admin.site.register(Unit, UnitAdmin)
admin.site.register(DerivedUnit)
admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(Substance, SubstanceAdmin)
admin.site.register(Compound, CompoundAdmin)
admin.site.register(Container)

