from django.contrib import admin
from .models import *


class ContainerAdmin(admin.ModelAdmin):
    list_display = ('compound', 'supplier', 'amount', 'amount_left', 'amount_unit', 'description')


# class CompoundAdmin(admin.ModelAdmin):
#     # inlines = []
#     list_display = ('substances',)


class CompoundInline(admin.TabularInline):
    model = Compound
    extra = 0


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 0


class SubstanceAdmin(admin.ModelAdmin):
    inlines = [
        ComponentInline
    ]
    list_display = ('names', 'formula', 'mol_weight')


admin.site.register(Unit)
admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(UnitCell)
admin.site.register(Structure)
admin.site.register(Substance, SubstanceAdmin)
admin.site.register(Component)
admin.site.register(Compound)
admin.site.register(Container)

