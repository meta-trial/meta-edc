from django.contrib.admin import SimpleListFilter
from edc_constants.constants import NO, YES

from meta_reports.models import Endpoints


class EndpointListFilter(SimpleListFilter):
    title = "Endpoint"
    parameter_name = "endpoint"

    def lookups(self, request, model_admin):
        return (
            (YES, YES),
            (NO, NO),
        )

    def queryset(self, request, queryset):
        if self.value() == YES:
            return queryset.filter(
                subject_identifier__in=Endpoints.objects.values_list(
                    "subject_identifier", flat=True
                )
            )
        if self.value() == YES:
            return queryset.exclude(
                subject_identifier__in=Endpoints.objects.values_list(
                    "subject_identifier", flat=True
                )
            )
        return queryset
