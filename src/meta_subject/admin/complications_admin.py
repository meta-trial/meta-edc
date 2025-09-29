from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..models import Complications
from .modeladmin import CrfModelAdminMixin


@admin.register(Complications, site=meta_subject_admin)
class ComplicationsAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    fieldsets = (
        ("Eye Examination", {"fields": ("cataracts", "fundoscopy")}),
        (
            "Foot Exam",
            {
                "fields": (
                    "achilles_tendon_reflex",
                    "foot_pin_prick",
                    "foot_light_touch",
                    "temperature_perception",
                )
            },
        ),
        (
            "Peripheral pulses",
            {"fields": ("dorsalis_pedis_pulse", "posterior_tibial_pulse")},
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )
