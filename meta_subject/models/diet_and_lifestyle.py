from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class DietAndLifestyle(CrfModelMixin, edc_models.BaseUuidModel):
    diet_and_lifestyle = models.CharField(
        verbose_name=(
            "Has the participant received the META3 " "approved diet and lifetsyle counseling?"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text="This response is not criteria for eligibility",
    )

    diet_and_lifestyle_duration = models.IntegerField(
        verbose_name=(
            "How much time was spent on the META3 "
            "approved diet and lifetsyle counseling with the patient?"
        ),
        null=True,
        blank=False,
        help_text="Report in minutes. This response is not criteria for eligibility",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinic follow up: Examination"
        verbose_name_plural = "Clinic follow up: Examination"
