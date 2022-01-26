from django.db import models

# TODO: add assessment of understanding section (P4?) and duration?
# TODO: diet and lifestyle discussion duration?
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE


class PartFourFieldsModelMixin(models.Model):

    # added 19/11/2021
    # TODO: "In the opinion of the clinican, has the participant fasted?"
    # TODO: the second measure is used for eligibility

    # fasting_opinion = models.CharField(
    #     verbose_name="In the opinion of the clinican, has the participant fasted?",
    #     max_length=15,
    #     choices=YES_NO_UNSURE,
    #     null=True,
    #     blank=False,
    # )

    # Assessment of understanding
    aou = models.CharField(
        verbose_name="Have the research staff assessed the subject's understanding of the study?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text="Using META3 approved assessment tool. This response is not criteria for eligibility",
    )

    aou_duration = models.IntegerField(
        verbose_name="How much time was spent on assessing the subject's understanding of the study?",
        null=True,
        blank=False,
        help_text="Report in minutes. This response is not criteria for eligibility",
    )

    aou_passed = models.CharField(
        verbose_name=(
            "Based on the META3 approved assessment tool, has the subject "
            "demonstrated sufficient understanding of the study to continue?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        blank=False,
        help_text="This response is not criteria for eligibility",
    )

    class Meta:
        abstract = True
