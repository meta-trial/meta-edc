from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.model_admin_simple_history import SimpleHistoryAdmin

from ..admin_site import meta_screening_admin
from ..forms import SubjectRefusalForm
from ..models import SubjectRefusal


@admin.register(SubjectRefusal, site=meta_screening_admin)
class SubjectRefusalAdmin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):

    form = SubjectRefusalForm

    autocomplete_fields = ["subject_screening"]

    post_url_on_delete_name = "screening_listboard_url"
    subject_listboard_url_name = "screening_listboard_url"
    subject_dashboard_url_name = "screening_listboard_url"

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "subject_screening",
                    "report_datetime",
                    "reason",
                    "other_reason",
                )
            },
        ],
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_screening",
        "report_datetime",
        "reason",
        "user_created",
        "created",
    )

    list_filter = ("report_datetime", "subject_screening__gender", "reason")

    search_fields = (
        "subject_screening__screening_identifier",
        "subject_screening__hospital_identifier",
        "subject_screening__initials",
    )

    radio_fields = {"reason": admin.VERTICAL}

    def get_subject_dashboard_url_kwargs(self, obj):
        return dict(screening_identifier=obj.screening_identifier)

    def view_on_site(self, obj):
        try:
            url = reverse(
                self.get_subject_dashboard_url_name(),
                kwargs=self.get_subject_dashboard_url_kwargs(obj),
            )
        except NoReverseMatch as e:
            if callable(super().view_on_site):
                url = super().view_on_site(obj)
            else:
                raise NoReverseMatch(f"{e}. See subject_dashboard_url_name for {repr(self)}.")
        return url
