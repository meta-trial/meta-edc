from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from django.utils.safestring import mark_safe

from ..admin_site import meta_subject_admin
from ..forms import MedicationAdherenceForm
from ..models import MedicationAdherence
from .modeladmin import CrfModelAdmin


description = """
<H5><B><font color="orange">Interviewer to read</font></B></H5>
<p>Drag the slider on the line below at
the point showing your best guess about how much study medication
you have taken in the last 14 days or in the last 28 days as
appropriate:<BR><BR>
<B>0%</B> means you have taken no study pills<BR>
<B>50%</B> means you have taken half of your study pills<BR>
<B>100%</B> means you have taken all your study pills<BR>
</p>
"""


@admin.register(MedicationAdherence, site=meta_subject_admin)
class MedicationAdherenceAdmin(CrfModelAdmin):

    form = MedicationAdherenceForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Visual Score",
            {
                "description": mark_safe(description),
                "fields": ("visual_score_slider", "visual_score_confirmed"),
            },
        ),
        (
            "Pill count",
            {
                "description": mark_safe(
                    "<H5><B><font color='orange'>Interviewer to read</font></B></H5>"
                    "<p>People may miss taking their "
                    "medicines for various reasons. What was the reason you "
                    "missed taking your pills the last time?</p>"
                ),
                "fields": (
                    "pill_count",
                    "last_missed_pill",
                    "missed_pill_reason",
                    "other_missed_pill_reason",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {"last_missed_pill": admin.VERTICAL}

    filter_horizontal = ("missed_pill_reason",)
