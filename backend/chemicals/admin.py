from django.contrib import admin
from .models import *


# Register your models here.

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


admin.site.register(Unit)
admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(Container)
admin.site.register(Substance, SubstanceAdmin)
admin.site.register(Compound, CompoundAdmin)
