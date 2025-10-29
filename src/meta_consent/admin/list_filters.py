from clinicedc_constants import NO, NOT_APPLICABLE, YES
from django.contrib.admin import SimpleListFilter
from edc_constants.choices import YES_NO_NA


class AgreesListFilter(SimpleListFilter):
    title = "Agrees"
    parameter_name = "agrees"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return YES_NO_NA

    def queryset(self, request, queryset):  # noqa: ARG002
        qs = None
        if self.value():
            if self.value() == YES:
                qs = queryset.filter(agrees_to_extension=YES)
            elif self.value() == NO:
                qs = queryset.filter(agrees_to_extension=NO)
            elif self.value() == NOT_APPLICABLE:
                qs = queryset.filter(agrees_to_extension=NOT_APPLICABLE)
        return qs
