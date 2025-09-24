from django.contrib import admin, messages
from django.core.exceptions import MultipleObjectsReturned
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_egfr.egfr import Egfr
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import (
    BloodResultFieldset,
    calculate_egfr_drop_fieldset,
    calculate_egfr_fieldset,
)
from edc_model_admin.history import SimpleHistoryAdmin
from edc_registration.models import RegisteredSubject
from edc_utils import get_utcnow
from edc_utils.round_up import round_half_away_from_zero
from edc_visit_schedule.constants import DAY1
from edc_visit_schedule.utils import is_baseline

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsRftForm
from ...models import BloodResultsRft, EgfrDropNotification, SubjectVisit
from ..modeladmin import CrfModelAdminMixin


@admin.register(BloodResultsRft, site=meta_subject_admin)
class BloodResultsRftAdmin(
    BloodResultsModelAdminMixin, CrfModelAdminMixin, SimpleHistoryAdmin
):
    form = BloodResultsRftForm
    actions = ("create_or_update_egfr_notification", "recalculate_egfr")
    fieldsets = (
        *BloodResultFieldset(
            BloodResultsRft.lab_panel,
            model_cls=BloodResultsRft,
            extra_fieldsets=[
                (5, calculate_egfr_fieldset),
                (6, calculate_egfr_drop_fieldset),
                (-1, action_fieldset_tuple),
            ],
            excluded_utest_ids=["egfr", "egfr_drop"],
        ).fieldsets,
    )

    def get_readonly_fields(self, request, obj=None) -> tuple[str, ...]:  # noqa: ARG002
        readonly_fields = super().get_readonly_fields(request)
        custom_fields = (
            "egfr_value",
            "egfr_units",
            "egfr_drop_value",
            "egfr_grade",
            "egfr_drop_units",
            "egfr_drop_grade",
            "summary",
        )
        return tuple(set(custom_fields + readonly_fields))

    @admin.action(permissions=["view"], description="Create or update eGFR notification")
    def create_or_update_egfr_notification(self, request, queryset):
        total = EgfrDropNotification.objects.all().count()
        for obj in queryset:
            obj.save()
        new_total = EgfrDropNotification.objects.all().count()
        messages.success(request, f"Created {new_total - total} new eGFR notifications.")

    @admin.action(permissions=["view"], description="Recalculate eGFR")
    def recalculate_egfr(self, request, queryset):
        updated = 0
        errors = 0
        for obj in queryset:
            if is_baseline(obj.related_visit):
                baseline_egfr_value = None
            else:
                baseline_visit = SubjectVisit.objects.get(
                    subject_identifier=obj.related_visit.subject_identifier,
                    visit_code=DAY1,
                    visit_code_sequence=0,
                )
                baseline_egfr_value = BloodResultsRft.objects.get(
                    subject_visit_id=baseline_visit.id
                ).egfr_value
            rs = RegisteredSubject.objects.get(
                subject_identifier=obj.related_visit.subject_identifier
            )
            egfr_options = dict(
                dob=rs.dob,
                gender=rs.gender,
                ethnicity=rs.ethnicity,
                value_threshold=45.0000,
                report_datetime=obj.report_datetime,
                baseline_egfr_value=baseline_egfr_value,
                formula_name="ckd-epi",
                reference_range_collection_name="meta",
                subject_visit=obj.related_visit,
                creatinine_units=obj.creatinine_units,
                creatinine_value=obj.creatinine_value,
                assay_datetime=obj.assay_datetime,
            )
            egfr = Egfr(percent_drop_threshold=20.0000, **egfr_options)
            if round_half_away_from_zero(obj.egfr_value, 4) != round_half_away_from_zero(
                egfr.egfr_value, 4
            ):
                obj.egfr_value = egfr.egfr_value
                obj.egfr_units = egfr.egfr_units
                obj.egfr_grade = egfr.egfr_grade
                obj.egfr_drop_value = egfr.egfr_drop_value
                obj.egfr_drop_units = egfr.egfr_drop_units
                obj.egfr_drop_grade = egfr.egfr_drop_grade
                obj.modified = get_utcnow()
                try:
                    obj.save_base()
                except MultipleObjectsReturned:
                    errors += 1
                    messages.add_message(
                        request,
                        messages.WARNING,
                        f"Unable to update {obj.subject_visit.subject_identifier} "
                        f"{obj.subject_visit.visit_code}"
                        f"{obj.subject_visit.visit_code_sequence}",
                    )
                else:
                    updated += 1
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Done. Updated {updated} documents with {errors} errors.",
        )
