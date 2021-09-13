from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin import TabularInlineMixin

from ..admin_site import meta_subject_admin
from ..forms import OtherArvRegimensDetailForm, OtherArvRegimensForm
from ..models import OtherArvRegimens, OtherArvRegimensDetail, PatientHistory
from .modeladmin import CrfModelAdmin


class OtherArvRegimensInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = OtherArvRegimensDetail
    form = OtherArvRegimensDetailForm
    extra = 1
    view_on_site = False
    autocomplete_fields = ["arv_regimen"]
    insert_after = "has_other_regimens"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        # formset.validate_min = True
        return formset

    fieldsets = (
        [
            "ARV Regimen History",
            {
                "description": (
                    "Do not include most recent two regimens reported on the "
                    f"`{PatientHistory._meta.verbose_name}` CRF"
                ),
                "fields": (
                    "arv_regimen",
                    "other_arv_regimen",
                    "arv_regimen_start_date",
                    "notes",
                ),
            },
        ],
    )


@admin.register(OtherArvRegimens, site=meta_subject_admin)
class OtherArvRegimensAdmin(CrfModelAdmin):

    form = OtherArvRegimensForm

    inlines = [OtherArvRegimensInlineAdmin]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime", "has_other_regimens")}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "has_other_regimens": admin.VERTICAL,
    }
