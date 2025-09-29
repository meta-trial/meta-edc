from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_screening_admin
from ..forms import (
    ScreeningPartTwoForm,
    calculated_fields,
    part_one_fields,
    part_three_fields,
)
from ..models import ScreeningPartTwo
from .fieldsets import (
    get_p3_screening_appt_update_fields,
    get_part_one_fieldset,
    get_part_three_fieldset,
    get_part_two_fieldset,
)
from .subject_screening_admin import SubjectScreeningAdmin


def get_fieldsets() -> tuple[
    tuple[str, dict],
    tuple[str, dict],
    tuple[str, dict],
    tuple[str, dict],
    tuple[str, dict],
]:
    return (
        get_part_one_fieldset(collapse=True),
        get_part_two_fieldset(),
        get_p3_screening_appt_update_fields(),
        get_part_three_fieldset(collapse=True),
        audit_fieldset_tuple,
    )


@admin.register(ScreeningPartTwo, site=meta_screening_admin)
class ScreeningPartTwoAdmin(SiteModelAdminMixin, SubjectScreeningAdmin):
    form = ScreeningPartTwoForm

    fieldsets = get_fieldsets()

    readonly_fields: tuple[str, ...] = (
        *part_one_fields,
        *part_three_fields,
        *calculated_fields,
    )
