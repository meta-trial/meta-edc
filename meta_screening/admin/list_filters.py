from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext as _
from edc_constants.constants import NO, NOT_APPLICABLE, PENDING, TBD, YES

from meta_screening.constants import PENDING_REPEAT


class EligibilityPending(admin.SimpleListFilter):
    title = _("P3 pending")

    parameter_name = "eligibility_pending"

    def lookups(self, request, model_admin):
        return (
            (PENDING, "Pending"),
            (PENDING_REPEAT, "Pending repeat GLU"),
        )

    def queryset(self, request, queryset):
        if self.value() == PENDING_REPEAT:
            return queryset.filter(
                eligible_part_one=YES,
                eligible_part_two=YES,
                eligible_part_three=TBD,
                part_three_report_datetime__isnull=False,
                repeat_glucose_opinion=YES,
            )
        if self.value() == PENDING:
            return queryset.filter(
                eligible_part_one=YES,
                eligible_part_two=YES,
                eligible_part_three=TBD,
                agree_to_p3=YES,
                p3_ltfu=NOT_APPLICABLE,
                part_three_report_datetime__isnull=True,
            )


class P3Ltfu(admin.SimpleListFilter):
    title = _("Contact for P3?")

    parameter_name = "p3_ltfu_custom"

    def lookups(self, request, model_admin):
        return (
            (YES, "Yes"),
            (NO, "No, lost contact"),
        )

    def queryset(self, request, queryset):
        if self.value() == YES:
            return queryset.filter(
                eligible_part_one=YES,
                eligible_part_two=YES,
                eligible_part_three=TBD,
                p3_ltfu=NOT_APPLICABLE,
            )
        if self.value() == NO:
            return queryset.filter(
                eligible_part_one=YES,
                eligible_part_two=YES,
                eligible_part_three=TBD,
                p3_ltfu=YES,
            )
        if self.value() == NO:
            return queryset.exclude(
                Q(eligible_part_one=TBD)
                | Q(eligible_part_two=TBD)
                | Q(eligible_part_three=TBD)
            )