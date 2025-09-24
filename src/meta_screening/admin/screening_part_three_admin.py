from copy import deepcopy

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_screening_admin
from ..forms import (
    ScreeningPartThreeForm,
    calculated_fields,
    part_one_fields,
    part_two_fields,
)
from ..models import ScreeningPartThree
from .fieldsets import (
    calculated_values_fieldset,
    comments_fieldset,
    get_part_one_fieldset,
    get_part_three_creatinine_fieldset,
    get_part_three_glucose_fieldset,
    get_part_three_hba1c_fieldset,
    get_part_three_pregnancy_fieldset,
    get_part_three_repeat_glucose_fieldset,
    get_part_three_report_datetime_fieldset,
    get_part_three_vitals_fieldset,
    get_part_two_fieldset,
)
from .list_filters import EligibilityPending, P3ApptListFilter, P3LtfuListFilter
from .subject_screening_admin import SubjectScreeningAdmin


def get_part_two_fieldset_without_contact_number() -> tuple[str, dict]:
    """Remove contact number from the part 2 fields"""
    part_two_name, part_two_dct = get_part_two_fieldset(collapse=True)
    part_two_dct = deepcopy(part_two_dct)
    part_two_dct["fields"] = [f for f in part_two_dct.get("fields") if f != "contact_number"]
    return part_two_name, part_two_dct


def get_fieldsets():
    return (
        get_part_one_fieldset(collapse=True),
        get_part_two_fieldset_without_contact_number(),
        get_part_three_report_datetime_fieldset(),
        get_part_three_vitals_fieldset(),
        get_part_three_pregnancy_fieldset(),
        get_part_three_glucose_fieldset(),
        get_part_three_repeat_glucose_fieldset(),
        get_part_three_creatinine_fieldset(),
        get_part_three_hba1c_fieldset(),
        comments_fieldset,
        calculated_values_fieldset,
        audit_fieldset_tuple,
    )


@admin.register(ScreeningPartThree, site=meta_screening_admin)
class ScreeningPartThreeAdmin(SiteModelAdminMixin, SubjectScreeningAdmin):
    form = ScreeningPartThreeForm

    fieldsets = get_fieldsets()

    list_filter = (
        # "part_three_report_datetime",
        "report_datetime",
        EligibilityPending,
        P3LtfuListFilter,
        P3ApptListFilter,
        "gender",
        "eligible",
        "eligible_part_one",
        "eligible_part_two",
        "eligible_part_three",
        "consented",
        "refused",
    )

    readonly_fields: tuple[str, ...] = (
        *part_one_fields,
        *(f for f in part_two_fields if f != "contact_number"),
        *calculated_fields,
    )
