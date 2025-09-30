from django.contrib import admin
from django.utils.safestring import mark_safe
from django_audit_fields import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import SpfqForm
from ..models import Spfq
from .modeladmin import CrfModelAdminMixin


@admin.register(Spfq, site=meta_subject_admin)
class SpfqAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    additional_instructions = mark_safe(
        "The Study Participant Feedback Questionnaire Toolkit (SPFQ) is a set of three "
        "brief validated patient questionnaires designed to capture patients’ experiences "
        "at the beginning, during, and end of each clinical study, independent of disease "
        "and treatment.<BR>"
        "<B><font color='orange'>Interviewer to read</font></B>: Thank you for your "
        "participation. Your experiences in this trial are important to us and we "
        "would like to hear about them. Your answers will help us improve future trials. "
        "There are no right or wrong answers. Your answers will be kept anonymous and "
        "will not impact your participation in this trial."
    )

    form = SpfqForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Section A: Your experience before you started the study",
            {
                "description": "Please select one response for each of the following items.",
                "fields": ("a01", "a02", "a03", "a04"),
            },
        ),
        (
            "Section B: Your experience during the trial",
            {
                "description": "Please select one response for each of the following items.",
                "fields": (
                    "b01",
                    "b02",
                    "b03",
                    "b04",
                    "b05",
                    "b06",
                    "b07",
                    "b08",
                    "b09",
                    "b10",
                ),
            },
        ),
        (
            "Section C: Your experience at the end of the trial",
            {
                "description": "Please select one response for each of the following items.",
                "fields": (
                    "c01",
                    "c02",
                    "c03",
                    "c04",
                    "c05",
                    "c06",
                    "c07",
                    "c08",
                    "c09",
                    "c10",
                ),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "a01": admin.VERTICAL,
        "a02": admin.VERTICAL,
        "a03": admin.VERTICAL,
        "a04": admin.VERTICAL,
        "b01": admin.VERTICAL,
        "b02": admin.VERTICAL,
        "b03": admin.VERTICAL,
        "b04": admin.VERTICAL,
        "b05": admin.VERTICAL,
        "b06": admin.VERTICAL,
        "b07": admin.VERTICAL,
        "b08": admin.VERTICAL,
        "b09": admin.VERTICAL,
        "b10": admin.VERTICAL,
        "c01": admin.VERTICAL,
        "c02": admin.VERTICAL,
        "c03": admin.VERTICAL,
        "c04": admin.VERTICAL,
        "c05": admin.VERTICAL,
        "c06": admin.VERTICAL,
        "c07": admin.VERTICAL,
        "c08": admin.VERTICAL,
        "c09": admin.VERTICAL,
        "c10": admin.VERTICAL,
    }
