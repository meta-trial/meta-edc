from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..models import HealthEconomics
from .modeladmin import CrfModelAdmin


@admin.register(HealthEconomics, site=meta_subject_admin)
class HealthEconomicsAdmin(CrfModelAdmin):

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Part 1: Education",
            {
                "fields": (
                    "occupation",
                    "education_in_years",
                    "education_certificate",
                    "primary_school",
                    "primary_school_in_years",
                    "secondary_school",
                    "secondary_school_in_years",
                    "higher_education",
                    "higher_education_in_years",
                )
            },
        ),
        (
            "Part 2: Household Income and Expenditures",
            {
                "fields": (
                    "welfare",
                    "income_per_month",
                    "household_income_per_month",
                    "is_highest_earner",
                    "highest_earner",
                    "food_per_month",
                    "accomodation_per_month",
                    "large_expenditure_year",
                    "buy_meds_month",
                    # "diabetic_expenditure_month",
                    # "diabetic_payee",
                    "hypertensive_expenditure_month",
                    "hypertensive_payee",
                    "arv_expenditure_month",
                    "arv_payee",
                    "meds_other_expenditure_month",
                    "meds_other_payee",
                    "expenditure_other_month",
                    "expenditure_other_detail",
                    "expenditure_other",
                    "expenditure_other_payee",
                    "healthcare_expenditure_month",
                )
            },
        ),
        (
            "Part 3: Work, Childcare, Transport",
            {
                "fields": (
                    "routine_activities",
                    "routine_activities_other",
                    "off_work_days",
                    "travel_time",
                    "hospital_time",
                    "lost_income",
                    "lost_income_amount",
                    "childcare",
                    "childcare_source",
                    "childcare_source_timeoff",
                    "transport_old",
                    "transport_cost",
                    "transport_barter",
                    "transport_borrow",
                    "health_insurance",
                    "health_insurance_pay",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "primary_school": admin.VERTICAL,
        "secondary_school": admin.VERTICAL,
        "higher_education": admin.VERTICAL,
        "welfare": admin.VERTICAL,
        "is_highest_earner": admin.VERTICAL,
        "buy_meds_month": admin.VERTICAL,
        "diabetic_payee": admin.VERTICAL,
        "hypertensive_payee": admin.VERTICAL,
        "arv_payee": admin.VERTICAL,
        "meds_other_payee": admin.VERTICAL,
        "expenditure_other_payee": admin.VERTICAL,
        "routine_activities": admin.VERTICAL,
        "lost_income": admin.VERTICAL,
        "childcare": admin.VERTICAL,
        "childcare_source": admin.VERTICAL,
        "transport_old": admin.VERTICAL,
        "transport_barter": admin.VERTICAL,
        "transport_borrow": admin.VERTICAL,
        "health_insurance": admin.VERTICAL,
        "expenditure_other_month": admin.VERTICAL,
    }
