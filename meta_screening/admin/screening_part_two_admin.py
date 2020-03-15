from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_screening_admin
from ..forms import (
    ScreeningPartTwoForm,
    part_one_fields,
    part_three_fields,
    calculated_fields,
)
from ..models import ScreeningPartTwo
from .fieldsets import (
    get_part_one_fieldset,
    get_part_two_fieldset,
    get_part_three_fieldset,
)
from .subject_screening_admin import SubjectScreeningAdmin


@admin.register(ScreeningPartTwo, site=meta_screening_admin)
class ScreeningPartTwoAdmin(SubjectScreeningAdmin):

    post_url_on_delete_name = "screening_dashboard_url"
    subject_listboard_url_name = "screening_listboard_url"

    form = ScreeningPartTwoForm

    fieldsets = (
        get_part_one_fieldset(collapse=True),
        get_part_two_fieldset(),
        get_part_three_fieldset(collapse=True),
        audit_fieldset_tuple,
    )

    readonly_fields = (*part_one_fields, *part_three_fields, *calculated_fields)
