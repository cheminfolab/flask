from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *


class TrackedAdmin(SimpleHistoryAdmin):
    """Admin for TrackedModel subclasses: shows history and records the acting admin."""
    readonly_fields = ('created_at', 'created_by', 'updated_at', 'updated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'symbol')


class ContainerAdmin(TrackedAdmin):
    list_display = ('compound', 'supplier', 'amount', 'amount_left', 'amount_unit', 'description')


class CompoundAdmin(TrackedAdmin):
    # inlines = []
    list_display = ('name', 'label')


class CompoundInline(admin.TabularInline):
    model = Compound
    extra = 0


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 0


class SubstanceAdmin(TrackedAdmin):
    inlines = [
        ComponentInline
    ]
    list_display = ('name', 'label', 'formula', 'mol_weight')


admin.site.register(Unit, UnitAdmin)
admin.site.register(Currency)
admin.site.register(UnitCell)
admin.site.register(Structure)
admin.site.register(Substance, SubstanceAdmin)
admin.site.register(Component, TrackedAdmin)
admin.site.register(Compound, CompoundAdmin)
admin.site.register(Container, ContainerAdmin)

