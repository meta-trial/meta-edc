from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from edc_constants.constants import HIGH, NORMAL
from edc_model_admin.list_filters import FutureDateListFilter, PastDateListFilter

from meta_subject.models import Glucose, GlucoseFbg

VERY_HIGH = "VERY_HIGH"


class GlucoseListFilter(SimpleListFilter):
    title = "Glucose"
    parameter_name = "glucose_value"
    model_cls = GlucoseFbg

    def lookups(self, request, model_admin):
        return (
            (NORMAL, "Normal"),
            (HIGH, "High"),
            (VERY_HIGH, "Very high"),
        )

    def queryset(self, request, queryset):
        qs = None
        if self.value():
            if self.value() == NORMAL:
                qs = self.model_cls.objects.filter(**{f"{self.parameter_name}__lt": 7.0})
            elif self.value() == HIGH:
                qs = self.model_cls.objects.filter(
                    Q(**{f"{self.parameter_name}__gte": 7.0}),
                    Q(**{f"{self.parameter_name}__lt": 11.1}),
                )
            elif self.value() == VERY_HIGH:
                qs = self.model_cls.objects.filter(**{f"{self.parameter_name}__gte": 11.1})
        return qs


class FbgListFilter(GlucoseListFilter):
    title = "FBG"
    parameter_name = "fbg_value"
    model_cls = Glucose


class OgttListFilter(SimpleListFilter):
    title = "OGTT"
    parameter_name = "ogtt_value"
    model_cls = Glucose

    def lookups(self, request, model_admin):
        return (
            (NORMAL, "Normal"),
            (HIGH, "High"),
        )

    def queryset(self, request, queryset):
        qs = None
        if self.value():
            if self.value() == NORMAL:
                qs = self.model_cls.objects.filter(**{f"{self.parameter_name}__lt": 11.1})
            elif self.value() == HIGH:
                qs = self.model_cls.objects.filter(**{f"{self.parameter_name}__gte": 11.1})
        return qs


class RefillStartDateListFilter(PastDateListFilter):
    title = "Refill start"

    parameter_name = "refill_start_datetime"
    field_name = "refill_start_datetime"


class RefillEndDateListFilter(FutureDateListFilter):
    title = "Refill end"

    parameter_name = "refill_end_datetime"
    field_name = "refill_end_datetime"
