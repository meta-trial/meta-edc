from django.db import models
from edc_constants.choices import YES_NO_TBD
from edc_constants.constants import TBD


class EligibilityModelMixin(models.Model):

    eligible_part_one = models.CharField(
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        editable=False,
        help_text="system calculated value",
    )

    reasons_ineligible_part_one = models.TextField(
        max_length=150, null=True, editable=False
    )

    eligible_part_two = models.CharField(
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        editable=False,
        help_text="system calculated value",
    )

    reasons_ineligible_part_two = models.TextField(
        max_length=150, null=True, editable=False
    )

    eligible_part_three = models.CharField(
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        editable=False,
        help_text="system calculated value",
    )

    reasons_ineligible_part_three = models.TextField(
        max_length=150, null=True, editable=False
    )

    class Meta:
        abstract = True
