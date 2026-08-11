from clinicedc_constants import NO, YES
from clinicedc_constants.choices import YES_NO
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class FinalAeClassificationSetListFilter(admin.SimpleListFilter):
    title = _("Final AE classification set")
    parameter_name = "final_ae_classification_set"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return YES_NO

    def queryset(self, request, queryset):  # noqa: ARG002
        if self.value() == YES:
            return queryset.filter(final_ae_classification__isnull=False)
        if self.value() == NO:
            return queryset.filter(final_ae_classification__isnull=True)
        return queryset


class HasAeTmgListFilter(admin.SimpleListFilter):
    title = _("Has AE TMG")
    parameter_name = "has_aetmg"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return YES_NO

    def queryset(self, request, queryset):  # noqa: ARG002
        if self.value() == YES:
            return queryset.filter(ae_tmg__isnull=False)
        if self.value() == NO:
            return queryset.filter(ae_tmg__isnull=True)
        return queryset
