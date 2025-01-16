from django.contrib.admin import SimpleListFilter
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NO, NOT_APPLICABLE, YES


class AgreesListFilter(SimpleListFilter):
    title = "Agrees"
    parameter_name = "agrees"

    def lookups(self, request, model_admin):
        return YES_NO_NA

    def queryset(self, request, queryset):
        qs = None
        if self.value():
            if self.value() == YES:
                qs = queryset.filter(agrees_to_extension=YES)
            elif self.value() == NO:
                qs = queryset.filter(agrees_to_extension=NO)
            elif self.value() == NOT_APPLICABLE:
                qs = queryset.filter(agrees_to_extension=NOT_APPLICABLE)
        return qs
