import pandas as pd
from django.contrib import admin, messages
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.list_filters import PastDateListFilter
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.admin.list_filters import SiteListFilter
from edc_utils import get_utcnow
from rangefilter.filters import DateRangeFilterBuilder

from meta_analytics.dataframes import get_last_imp_visits_df

from ..admin_site import meta_reports_admin
from ..models import LastImpRefill


class ImpVisitDateListFilter(PastDateListFilter):
    title = "IMP visit date"

    parameter_name = "imp_visit_date"
    field_name = "imp_visit_date"


class NextApptDateListFilter(PastDateListFilter):
    title = "Next appt date"

    parameter_name = "next_appt_date"
    field_name = "next_appt_date"


def update_report(modeladmin, request, queryset):  # noqa: ARG001
    now = get_utcnow()
    modeladmin.model.objects.all().delete()
    df = get_last_imp_visits_df()
    if not df.empty:
        data = [
            modeladmin.model(
                subject_identifier=row["subject_identifier"],
                site_id=row["site_id"],
                imp_visit_date=(
                    None if pd.isna(row["imp_visit_date"]) else row["imp_visit_date"]
                ),
                imp_visit_code=row["imp_visit_code"],
                next_appt_date=(
                    None if pd.isna(row["next_appt_datetime"]) else row["next_appt_datetime"]
                ),
                next_visit_code=(
                    None if pd.isna(row["next_visit_code"]) else row["next_visit_code"]
                ),
                days_since=row["days_since"].days,
                days_until=None if pd.isna(row["days_until"]) else row["days_until"].days,
                visit_code=(
                    None if pd.isna(row["imp_visit_code"]) else str(int(row["imp_visit_code"]))
                ),
                visit_code_sequence=(
                    None if pd.isna(row["imp_visit_code"]) else row["imp_visit_code"] % 1
                ),
                report_model=modeladmin.model._meta.label_lower,
                created=now,
            )
            for _, row in df.iterrows()
        ]
        created = len(modeladmin.model.objects.bulk_create(data))
        messages.success(request, f"{created} records were successfully created.")


@admin.register(LastImpRefill, site=meta_reports_admin)
class LastImpRefillAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    include_note_column = False

    change_list_title = "List of most recent IMP refills per subject"

    change_list_note = mark_safe(  # noqa: S308
        render_to_string("meta_reports/last_imp_refill/changelist_note.html")
    )  # nosec B308, B703

    actions = (update_report,)

    list_display = (
        "dashboard",
        "subject_identifier",
        "imp_visit_code",
        "imp_visit_date",
        "days_since",
        "next_visit_code",
        "next_appt_date",
        "days_until",
        "created",
    )

    list_filter = (
        ("imp_visit_date", DateRangeFilterBuilder()),
        ("next_appt_date", DateRangeFilterBuilder()),
        "imp_visit_code",
        "next_visit_code",
        SiteListFilter,
    )

    search_fields = ("subject_identifier",)

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        if qs.count() == 0:
            update_report(self, request, None)
            qs = super().get_queryset(request)
        return qs

    def dataframe_to_model(self):
        now = get_utcnow()
        self.model.objects.all().delete()
        created = 0
        df = get_last_imp_visits_df()
        if not df.empty:
            data = [
                self.model(
                    subject_identifier=row["subject_identifier"],
                    site_id=row["site_id"],
                    imp_visit_date=row["imp_visit_date"],
                    imp_visit_code=row["imp_visit_code"],
                    next_appt_date=row["next_appt_datetime"],
                    next_visit_code=row["next_visit_code"],
                    days_since=row["days_since"],
                    days_until=row["days_until"],
                    visit_code=str(int(row["imp_visit_code"])),
                    visit_code_sequence=row["imp_visit_code"] % 1,
                    report_model=self.model._meta.label_lower,
                    created=now,
                )
                for _, row in df.iterrows()
            ]
            created = len(self.model.objects.bulk_create(data))
        return created

    def get_search_results(self, request, queryset, search_term):
        value = None
        fldname = None
        search_term = search_term.replace(" ", "")
        operators = {">=": "gte", "<=": "lte", "<": "lt", ">": "gt"}
        if op := [op for op in operators if op in search_term]:
            op = op[0]
            fldname, value = search_term.split(op)
            try:
                fldcls = self.model._meta.get_field(fldname)
            except FieldDoesNotExist:
                fldname = None
            else:
                if isinstance(fldcls, (models.IntegerField,)):
                    try:
                        value = int(value)
                    except ValueError:
                        value = None
                elif isinstance(fldcls, (models.FloatField,)):
                    try:
                        value = float(value)
                    except ValueError:
                        value = None
        if (
            value is not None
            and fldname
            and fldname in ["days_until", "days_since", "imp_visit_code", "next_visit_code"]
        ):
            queryset, use_distinct = super().get_search_results(request, queryset, None)
            queryset = queryset.filter(**{f"{fldname}__{operators[op]}": value})
        else:
            queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct
