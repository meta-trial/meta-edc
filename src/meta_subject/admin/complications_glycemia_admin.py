from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import ComplicationsGlycemiaForm
from ..models import ComplicationsGlycemia
from .modeladmin import CrfModelAdminMixin


@admin.register(ComplicationsGlycemia, site=meta_subject_admin)
class ComplicationsGlycemiaAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    form = ComplicationsGlycemiaForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                )
            },
        ),
        (
            "Eye examination",
            {
                "fields": (
                    "cataracts",
                    "fundoscopy",
                )
            },
        ),
        (
            "Foot examination",
            {
                "fields": (
                    "foot_skin_condition",
                    "foot_fungal_infection",
                    "foot_sores",
                    "foot_callouses",
                )
            },
        ),
        (
            "Peripheral pulses and reflexes",
            {
                "fields": (
                    "dp_pulse",
                    "pt_pulse",
                    "at_reflex",
                )
            },
        ),
        (
            "Neuropathy Disability Score (NDS)",
            {
                "fields": (
                    "nds_vpt_right",
                    "nds_vpt_left",
                    "nds_tp_right",
                    "nds_tp_left",
                    "nds_pp_right",
                    "nds_pp_left",
                    "nds_achilles_reflex_right",
                    "nds_achilles_reflex_left",
                )
            },
        ),
        (
            "10-g monofilament test",
            {
                "fields": (
                    "first_metatarsal_right",
                    "first_metatarsal_left",
                    "third_metatarsal_right",
                    "third_metatarsal_left",
                    "fifth_metatarsal_right",
                    "fifth_metatarsal_left",
                    "plantar_surface_right",
                    "plantar_surface_left",
                )
            },
        ),
        (
            "Diabetic Neuropathy Symptom Score",
            {
                "fields": (
                    "dns_walking",
                    "dns_burning",
                    "dns_tingling",
                    "dns_numbness",
                )
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "at_reflex": admin.VERTICAL,
        "cataracts": admin.VERTICAL,
        "dns_burning": admin.VERTICAL,
        "dns_numbness": admin.VERTICAL,
        "dns_tingling": admin.VERTICAL,
        "dns_walking": admin.VERTICAL,
        "dp_pulse": admin.VERTICAL,
        "fifth_metatarsal_right": admin.VERTICAL,
        "fifth_metatarsal_left": admin.VERTICAL,
        "first_metatarsal_right": admin.VERTICAL,
        "first_metatarsal_left": admin.VERTICAL,
        "foot_callouses": admin.VERTICAL,
        "foot_fungal_infection": admin.VERTICAL,
        "foot_skin_condition": admin.VERTICAL,
        "foot_sores": admin.VERTICAL,
        "fundoscopy": admin.VERTICAL,
        "nds_achilles_reflex_left": admin.VERTICAL,
        "nds_achilles_reflex_right": admin.VERTICAL,
        "nds_pp_left": admin.VERTICAL,
        "nds_pp_right": admin.VERTICAL,
        "nds_tp_left": admin.VERTICAL,
        "nds_tp_right": admin.VERTICAL,
        "nds_vpt_left": admin.VERTICAL,
        "nds_vpt_right": admin.VERTICAL,
        "plantar_surface_left": admin.VERTICAL,
        "plantar_surface_right": admin.VERTICAL,
        "pt_pulse": admin.VERTICAL,
        "third_metatarsal_right": admin.VERTICAL,
        "third_metatarsal_left": admin.VERTICAL,
    }
