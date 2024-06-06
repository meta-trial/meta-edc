from dateutil.relativedelta import relativedelta
from django.contrib.admin import SimpleListFilter
from django.db.models import Q, QuerySet
from django.utils.translation import gettext as _
from edc_constants.constants import HIGH, NORMAL
from edc_model_admin.list_filters import FutureDateListFilter, PastDateListFilter
from edc_utils import get_utcnow

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


LT_60_DAYS = "LT_60_DAYS"
GTE_60_TO_90_DAYS = "GTE_60_TO_90_DAYS"
GTE_90_TO_180_DAYS = "GTE_90_TO_180_DAYS"
GTE_180 = "GTE_180"


class LastSeenDaysListFilter(SimpleListFilter):
    """On study, last appointment was ..."""

    title = "Last seen (days)"

    parameter_name = "last_seen_days"
    field_name = "appt_datetime"

    def lookups(self, request, model_admin) -> tuple:
        return (
            (LT_60_DAYS, _("0-60 days")),
            (GTE_60_TO_90_DAYS, _("60-90 days")),
            (GTE_90_TO_180_DAYS, _("90-180 days")),
            (GTE_180, _("180+ days")),
        )

    def queryset(self, request, queryset) -> QuerySet | None:
        now = get_utcnow().replace(second=59, hour=23, minute=59)
        qs = None
        if self.value() == LT_60_DAYS:
            qs = queryset.filter(
                **{
                    f"{self.field_name}__gt": now - relativedelta(days=60),
                    f"{self.field_name}__lte": now - relativedelta(days=0),
                },
            ).order_by(self.field_name)
        elif self.value() == GTE_60_TO_90_DAYS:
            qs = queryset.filter(
                **{
                    f"{self.field_name}__gt": now - relativedelta(days=90),
                    f"{self.field_name}__lte": now - relativedelta(days=60),
                },
            ).order_by(self.field_name)
        elif self.value() == GTE_90_TO_180_DAYS:
            qs = queryset.filter(
                **{
                    f"{self.field_name}__gt": now - relativedelta(days=180),
                    f"{self.field_name}__lte": now - relativedelta(days=90),
                },
            ).order_by(self.field_name)
        elif self.value() == GTE_180:
            qs = queryset.filter(
                **{
                    f"{self.field_name}__lte": now - relativedelta(days=180),
                },
            ).order_by(self.field_name)
        return qs
