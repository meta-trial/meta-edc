from typing import Tuple

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

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


def get_fieldsets() -> Tuple[
    Tuple[str, dict], Tuple[str, dict], Tuple[str, dict], Tuple[str, dict], Tuple[str, dict]
]:
    return (
        get_part_one_fieldset(collapse=True),
        get_part_two_fieldset(),
        get_p3_screening_appt_update_fields(),
        get_part_three_fieldset(collapse=True),
        audit_fieldset_tuple,
    )


@admin.register(ScreeningPartTwo, site=meta_screening_admin)
class ScreeningPartTwoAdmin(SubjectScreeningAdmin):

    post_url_on_delete_name = "screening_dashboard_url"
    subject_listboard_url_name = "screening_listboard_url"

    form = ScreeningPartTwoForm

    fieldsets = get_fieldsets()

    readonly_fields = (
        *part_one_fields,
        *part_three_fields,
        *calculated_fields,
    )
