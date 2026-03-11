from clinicedc_constants import NO, YES
from django.contrib.admin import SimpleListFilter

from meta_reports.models import Endpoints


class EndpointListFilter(SimpleListFilter):
    title = "Endpoint"
    parameter_name = "endpoint"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return (
            (YES, YES),
            (NO, NO),
        )

    def queryset(self, request, queryset):  # noqa: ARG002
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


class IsOffScheduleListFilter(SimpleListFilter):
    title = "Offschedule"
    parameter_name = "offschedule"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return (
            (YES, YES),
            (NO, NO),
        )

    def queryset(self, request, queryset):  # noqa: ARG002
        if self.value() == YES:
            return queryset.filter(offschedule_datetime__isnull=False)

        if self.value() == YES:
            return queryset.filter(offschedule_datetime__isnull=True)
        return queryset
