from django.db import models
from edc_constants.choices import YES_NO_TBD
from edc_constants.constants import TBD
from edc_screening.model_mixins import (
    EligibilityModelMixin as BaseEligibilityModelMixin,
)

from ..eligibility import MetaEligibility


class EligibilityModelMixin(BaseEligibilityModelMixin):

    eligibility_cls = MetaEligibility

    eligible_part_one = models.CharField(
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        editable=False,
        help_text="system calculated value",
    )

    reasons_ineligible_part_one = models.TextField(max_length=150, null=True, editable=False)

    eligible_part_two = models.CharField(
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        editable=False,
        help_text="system calculated value",
    )

    reasons_ineligible_part_two = models.TextField(max_length=150, null=True, editable=False)

    eligible_part_three = models.CharField(
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        editable=False,
        help_text="system calculated value",
    )

    reasons_ineligible_part_three = models.TextField(max_length=150, null=True, editable=False)

    def get_report_datetime_for_eligibility_datetime(self):
        return self.part_three_report_datetime

    class Meta:
        abstract = True
