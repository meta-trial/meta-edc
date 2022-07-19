from django.contrib import admin
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django_audit_fields.admin import audit_fieldset_tuple
from edc_constants.constants import YES
from edc_dashboard.url_names import url_names
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import meta_screening_admin
from ..eligibility import MetaEligibility, format_reasons_ineligible
from ..forms import SubjectScreeningForm
from ..models import SubjectScreening
from .fieldsets import (
    calculated_values_fieldset,
    get_p3_screening_appt_update_fields,
    get_part_one_fieldset,
    get_part_three_fieldset,
    get_part_two_fieldset,
)
from .list_filters import EligibilityPending, P3LtfuListFilter


@admin.register(SubjectScreening, site=meta_screening_admin)
class SubjectScreeningAdmin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):

    form = SubjectScreeningForm
    list_per_page = 15
    post_url_on_delete_name = "screening_listboard_url"
    subject_listboard_url_name = "screening_listboard_url"

    additional_instructions = (
        "Patients must meet ALL of the inclusion criteria and NONE of the "
        "exclusion criteria in order to proceed to the final screening stage"
    )

    fieldsets = (
        get_part_one_fieldset(),
        get_part_two_fieldset(),
        get_p3_screening_appt_update_fields(),
        get_part_three_fieldset(),
        calculated_values_fieldset,
        audit_fieldset_tuple,
    )

    list_display = (
        "screening_identifier",
        "eligiblity_status",
        "demographics",
        "reasons",
        "report_datetime",
        "p3_appt",
        "p3_repeat_appt",
        "user_created",
        "created",
    )

    list_filter = (
        "report_datetime",
        "part_three_report_datetime",
        EligibilityPending,
        P3LtfuListFilter,
        "gender",
        "eligible",
        "eligible_part_one",
        "eligible_part_two",
        "eligible_part_three",
        "consented",
        "refused",
    )

    search_fields = (
        "screening_identifier",
        "subject_identifier",
        "hospital_identifier",
        "initials",
        "reasons_ineligible",
    )

    readonly_fields = (
        # calculated values
        "calculated_bmi_value",
        "calculated_egfr_value",
        "converted_fbg_value",
        "converted_fbg2_value",
        "converted_creatinine_value",
        "converted_ogtt_value",
        "converted_ogtt2_value",
        "inclusion_a",
        "inclusion_b",
        "inclusion_c",
        "inclusion_d",
    )

    radio_fields = {
        "acute_condition": admin.VERTICAL,
        "acute_metabolic_acidosis": admin.VERTICAL,
        "advised_to_fast": admin.VERTICAL,
        "agree_to_p3": admin.VERTICAL,
        "alcoholism": admin.VERTICAL,
        "already_fasted": admin.VERTICAL,
        "art_six_months": admin.VERTICAL,
        "congestive_heart_failure": admin.VERTICAL,
        "continue_part_two": admin.VERTICAL,
        "creatinine_performed": admin.VERTICAL,
        "creatinine_units": admin.VERTICAL,
        "ethnicity": admin.VERTICAL,
        "fasting": admin.VERTICAL,
        "fbg2_units": admin.VERTICAL,
        "fbg_units": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "has_dm": admin.VERTICAL,
        "hba1c_performed": admin.VERTICAL,
        "hiv_pos": admin.VERTICAL,
        "liver_disease": admin.VERTICAL,
        "lives_nearby": admin.VERTICAL,
        "meta_phase_two": admin.VERTICAL,
        "metformin_sensitivity": admin.VERTICAL,
        "ogtt2_units": admin.VERTICAL,
        "ogtt_units": admin.VERTICAL,
        "on_dm_medication": admin.VERTICAL,
        "on_rx_stable": admin.VERTICAL,
        "p3_ltfu": admin.VERTICAL,
        "pregnant": admin.VERTICAL,
        "renal_function_condition": admin.VERTICAL,
        "repeat_fasting": admin.VERTICAL,
        "repeat_glucose_opinion": admin.VERTICAL,
        "repeat_glucose_performed": admin.VERTICAL,
        "screening_consent": admin.VERTICAL,
        "selection_method": admin.VERTICAL,
        "severe_htn": admin.VERTICAL,
        "staying_nearby_12": admin.VERTICAL,
        "staying_nearby_6": admin.VERTICAL,
        "tissue_hypoxia_condition": admin.VERTICAL,
        "unsuitable_agreed": admin.VERTICAL,
        "unsuitable_for_study": admin.VERTICAL,
        "urine_bhcg_performed": admin.VERTICAL,
        "urine_bhcg_value": admin.VERTICAL,
        "vl_undetectable": admin.VERTICAL,
    }

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    @staticmethod
    def demographics(obj=None):
        data = [
            f"{obj.get_gender_display()} {obj.age_in_years}yrs",
            f"Initials: {obj.initials.upper()}<BR>",
            f"Hospital ID: {obj.hospital_identifier}",
        ]
        if obj.repeat_glucose_opinion == YES:
            data.append(f"Contact #: {obj.contact_number or '--'}")
        return format_html("<BR>".join(data))

    def reasons(self, obj=None):
        if not obj.reasons_ineligible:
            return self.dashboard(obj)
        return format_reasons_ineligible(obj.reasons_ineligible)

    def eligiblity_status(self, obj=None):
        eligibility = MetaEligibility(obj, update_model=False)
        screening_listboard_url = reverse(
            url_names.get(self.subject_listboard_url_name), args=(obj.screening_identifier,)
        )
        context = dict(
            title=_("Go to screening listboard"),
            url=f"{screening_listboard_url}?q={obj.screening_identifier}",
            label="Screening",
        )
        button = render_to_string("dashboard_button.html", context=context)
        return format_html(button + "<BR>" + eligibility.eligibility_status(add_urls=True))

    def dashboard(self, obj=None, label=None):
        try:
            url = reverse(
                self.get_subject_dashboard_url_name(),
                kwargs=self.get_subject_dashboard_url_kwargs(obj),
            )
        except NoReverseMatch:
            url = reverse(url_names.get("screening_listboard_url"), kwargs={})
            context = dict(
                title=_("Go to screening listboard"),
                url=f"{url}?q={obj.screening_identifier}",
                label=label,
            )
        else:
            context = dict(title=_("Go to subject dashboard"), url=url, label=label)
        return render_to_string("dashboard_button.html", context=context)
