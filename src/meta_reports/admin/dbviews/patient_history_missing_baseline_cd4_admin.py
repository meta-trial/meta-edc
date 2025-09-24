import contextlib

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from edc_appointment.models import Appointment
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter
from edc_visit_schedule.constants import DAY1

from ...admin_site import meta_reports_admin
from ...models import PatientHistoryMissingBaselineCd4


@admin.register(PatientHistoryMissingBaselineCd4, site=meta_reports_admin)
class PatientHistoryMissingBaselineCd4Admin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    ordering = ("site", "subject_identifier")
    list_display = (
        "dashboard",
        "subject_identifier",
        "cd4",
        "cd4_date",
        "site",
        "user_created",
        "user_modified",
        "modified",
    )

    list_filter = (ScheduleStatusListFilter,)

    search_fields = ("subject_identifier",)

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
