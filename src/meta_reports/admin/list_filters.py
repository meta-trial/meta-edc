import contextlib
import operator
from functools import reduce

from clinicedc_constants import NO, YES
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from meta_reports.models import Endpoints


class EndpointListFilter(SimpleListFilter):
    title = "Reached endpoint"
    parameter_name = "endpoint_all"

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
        if self.value() == NO:
            return queryset.exclude(
                subject_identifier__in=Endpoints.objects.values_list(
                    "subject_identifier", flat=True
                )
            )
        return queryset


class OnlyEndpointListFilter(SimpleListFilter):
    title = "Only endpoints"
    parameter_name = "only_endpoint"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return (
            (YES, YES),
            (NO, NO),
        )

    def queryset(self, request, queryset):  # noqa: ARG002
        if self.value() == YES:
            conditions = [
                Q(subject_identifier=obj.subject_identifier) & Q(visit_code=obj.visit_code)
                for obj in Endpoints.objects.all()
            ]
            conditions = reduce(operator.or_, conditions)
            return queryset.filter(conditions).order_by("subject_identifier", "visit_code")
        return queryset

    @staticmethod
    def get_endpoint(obj):
        endpoint_obj = None
        with contextlib.suppress(ObjectDoesNotExist):
            endpoint_obj = Endpoints.objects.get(
                subject_identifier=obj.subject_identifier,
                visit_code=obj.visit_code,
            )
        return endpoint_obj


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
