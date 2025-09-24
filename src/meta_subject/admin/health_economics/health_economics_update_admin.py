from django.contrib import admin
from django.utils.translation import gettext as _
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import meta_subject_admin
from ...forms import HealthEconomicsUpdateForm
from ...models import HealthEconomicsUpdate
from ..modeladmin import CrfModelAdminMixin


@admin.register(HealthEconomicsUpdate, site=meta_subject_admin)
class HealthEconomicsUpdateAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    form = HealthEconomicsUpdateForm

    additional_instructions = _(
        """We want to learn about the household and we use these
        questions to get an understanding of wealth and opportunities
        in the community. A person or persons (people/ members) who share
        the same kitchen (pot), live together, and run the household
        expenditure from the same income is known as a 'household'. Household
        members should be identified on the basis that they shared a place of
        living together most of time for the past one year. When it is
        difficult to demarcate 'most of the time', living together for the
        past six months or more should be used to find out whether or not
        the person is a household member. For polygamous households, the
        household head should think about all the households and respond
        with respect to all households."""
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                )
            },
        ),
        (
            "A: Household and head of household",
            {
                "fields": (
                    "hh_count",
                    "hh_minors_count",
                    "hoh",
                    "relationship_to_hoh",
                    "relationship_to_hoh_other",
                ),
            },
        ),
        (
            "B: Rooms and beds in your household",
            {
                "description": _(
                    "Before asking about household income, we would first like"
                    "to know about the number of rooms in the home and number of beds. "
                ),
                "fields": (
                    "rooms",
                    "bedrooms",
                    "beds",
                ),
            },
        ),
        (
            "C: Household income",
            {
                "description": _(
                    "Now, I will ask about income for the household from paid work"
                    "or other sources. Please think of the total income for the "
                    "household, including income from all household members "
                    "as defined above. I know it may be difficult to estimate, "
                    "but please do try to give amounts as accurately as possible. "
                    "Please note that all information will be kept strictly "
                    "confidential. This information is important to assess overall "
                    "health and well-being of people in your household, compared "
                    "to other similar households."
                ),
                "fields": (
                    "avg_income",
                    "avg_income_value_known",
                    "avg_income_value",
                    "external_dependents",
                    "financial_status",
                ),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "hoh": admin.VERTICAL,
        "relationship_to_hoh": admin.VERTICAL,
        "avg_income": admin.VERTICAL,
        "avg_income_value_known": admin.VERTICAL,
        "financial_status": admin.VERTICAL,
    }
