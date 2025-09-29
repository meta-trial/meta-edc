import contextlib

from django.apps import apps as django_apps
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from edc_appointment.models import Appointment
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.list_filters import ReportDateListFilter
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter
from edc_visit_schedule.constants import DAY1

from ...admin_site import meta_reports_admin
from ...models import ImpSubstitutions


@admin.register(ImpSubstitutions, site=meta_reports_admin)
class ImpSubstitutionsAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    ordering = ("site", "subject_identifier")
    list_display = (
        "dashboard",
        "render_button",
        "subject",
        "sid",
        "dispensed_sid",
        "report_date",
        "arm_match",
        "allocated_date",
        "user_created",
        "user_modified",
        "modified",
    )

    list_filter = (
        "arm_match",
        ScheduleStatusListFilter,
        ReportDateListFilter,
        "allocated_datetime",
    )

    search_fields = ("subject_identifier", "sid", "dispensed_sid")

    def dashboard(self, obj=None, label=None) -> str:
        kwargs = self.get_subject_dashboard_url_kwargs(obj)
        with contextlib.suppress(ObjectDoesNotExist):
            kwargs.update(
                appointment=str(
                    Appointment.objects.get(
                        subject_identifier=obj.subject_identifier,
                        visit_code=DAY1,
                        visit_code_sequence=0,
                    ).id
                )
            )
        url = reverse(self.get_subject_dashboard_url_name(obj=obj), kwargs=kwargs)
        context = dict(title=_("Go to subject's dashboard@1000"), url=url, label=label)
        return render_to_string("edc_subject_dashboard/dashboard_button.html", context=context)

    @admin.display(description="Subject", ordering="subject_identifier")
    def subject(self, obj):
        return obj.subject_identifier

    @admin.display(description="Allocated", ordering="allocated_datetime")
    def allocated_date(self, obj=None):
        return obj.allocated_datetime.date() if obj.allocated_datetime else None

    @admin.display(description="Update")
    def render_button(self, obj=None):
        crf_model_cls = django_apps.get_model("meta_pharmacy", "substitutions")
        url = reverse(
            f"meta_pharmacy_admin:{crf_model_cls._meta.label_lower.replace('.', '_')}_change",
            args=(obj.original_id,),
        )
        url = (
            f"{url}?next={self.admin_site.name}:"
            f"{self.model._meta.label_lower.replace('.', '_')}_changelist"
        )
        title = _("View %(verbose_name)s").format(
            verbose_name=crf_model_cls._meta.verbose_name
        )
        label = _("View")
        return render_to_string(
            "edc_qareports/columns/change_button.html",
            context=dict(title=title, url=url, label=label),
        )

    @admin.display(description="Report date", ordering="report_datetime")
    def report_date(self, obj) -> str | None:
        if obj.report_datetime:
            return obj.report_datetime.date()
        return None
