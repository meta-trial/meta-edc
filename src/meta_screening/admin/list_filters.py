from clinicedc_constants import NO, NOT_APPLICABLE, PENDING, TBD, YES
from django.contrib import admin
from django.db.models import Q
from edc_appointment.admin import AppointmentListFilter

from ..constants import PENDING_REPEAT


class EligibilityPending(admin.SimpleListFilter):
    title = "P3 pending"

    parameter_name = "eligibility_pending"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return (
            (PENDING, "Pending"),
            (PENDING_REPEAT, "Pending repeat GLU"),
        )

    def queryset(self, request, queryset):  # noqa: ARG002
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
        return queryset


class P3LtfuListFilter(admin.SimpleListFilter):
    title = "Contact for P3?"

    parameter_name = "p3_ltfu_custom"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return (
            (YES, "Yes"),
            (NO, "No, lost contact"),
        )

    def queryset(self, request, queryset):  # noqa: ARG002
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
        return queryset


class P3ApptListFilter(AppointmentListFilter):
    title = "Part 3 appointment"
    parameter_name = "p3_appt_datetime"
    field_name = "appt_datetime"

    @property
    def extra_queryset_options(self):
        return dict(
            eligible_part_one=YES,
            eligible_part_two=YES,
            eligible_part_three=TBD,
        )
