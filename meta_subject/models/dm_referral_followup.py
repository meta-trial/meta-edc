from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.html import format_html
from edc_adherence.choices import MISSED_PILLS
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField

from meta_lists.models import (
    Complications,
    DmMedications,
    DmTreatments,
    HealthcareWorkers,
    Investigations,
)

from ..model_mixins import CrfModelMixin


class DmReferralFollowup(CrfModelMixin, BaseUuidModel):
    referral_date = models.DateField(
        verbose_name="Date of referral to diabetes clinic",
    )

    # Diabetes clinic attendance
    attended = models.CharField(
        verbose_name=(
            "Did you attend the diabetes clinic following referral from the META Trial"
        ),
        choices=YES_NO,
        max_length=25,
    )

    not_attended_reason = models.TextField(
        verbose_name=(
            "If 'No', please provide a reason for not seeking further care or follow up?"
        ),
        null=True,
        blank=True,
    )

    facility_attended = models.CharField(
        verbose_name="If ‘Yes’, please give the name of the facility you attended",
        max_length=50,
        null=True,
        blank=True,
    )

    attended_date = models.DateField(
        verbose_name="What was the date you attended the health facility named above?",
        null=True,
        blank=True,
    )

    healthcare_workers = models.ManyToManyField(
        HealthcareWorkers,
        verbose_name="What type of health care worker did you see?",
        blank=True,
    )

    other_healthcare_workers = OtherCharField(
        verbose_name="If other 'healthcare worker', please specify ...",
        null=True,
        blank=True,
    )

    # investigations
    investigations_performed = models.CharField(
        verbose_name="Were any further investigations conducted at this visit?",
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        max_length=25,
    )

    investigations = models.ManyToManyField(
        Investigations,
        verbose_name="If ‘Yes’, please indicate what investigations were conducted.",
        blank=True,
    )

    other_investigations = OtherCharField(
        verbose_name="If other 'investigations', please specify ...",
        null=True,
        blank=True,
    )

    complications_checks_performed = models.CharField(
        verbose_name=(
            "Was the patient checked for diabetes related complications at this visit?"
        ),
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        max_length=25,
    )
    complications_checks = models.ManyToManyField(
        Complications,
        verbose_name="If 'Yes, which diabetes related complications were checked for?",
        blank=True,
    )

    other_complications_checks = OtherCharField(
        verbose_name=(
            "If other 'diabetes related complications checked for ', please specify ..."
        ),
        null=True,
        blank=True,
    )

    # dm treatment

    treatment_prescribed = models.CharField(
        verbose_name="Was any treatment prescribed at this visit?",
        choices=YES_NO_NA,
        max_length=25,
        default=NOT_APPLICABLE,
    )
    dm_treatments = models.ManyToManyField(
        DmTreatments,
        verbose_name="What treatment was prescribed?",
        blank=True,
    )

    on_dm_medications = models.CharField(
        verbose_name="Are you currently taking any drug therapy for diabetes?",
        choices=YES_NO,
        max_length=25,
    )

    dm_medications_init_date = models.DateField(
        verbose_name="If ‘Yes’, please give the date when drug treatment was started.",
        null=True,
        blank=True,
    )

    dm_medications = models.ManyToManyField(
        DmMedications,
        verbose_name=(
            "If ‘Yes’, please indicate which diabetes drug "
            "treatments you are currently taking."
        ),
        blank=True,
    )

    other_dm_medications = OtherCharField(
        verbose_name="If other 'drug treatments', please specify ...",
        null=True,
        blank=True,
    )

    # Diabetes Medication Adherence

    medications_adherent = models.CharField(
        verbose_name="Are you taking the diabetes drug treatments regularly, i.e. every day?",
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        max_length=25,
    )

    visual_score_slider = models.CharField(
        verbose_name="Visual score",
        max_length=3,
        help_text="%",
        null=True,
        blank=True,
    )

    visual_score_confirmed = models.IntegerField(
        verbose_name=format_html(
            "<B><font color='orange'>Interviewer</font></B>: "
            "please transcribe the score indicated from above."
        ),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="%",
        null=True,
        blank=True,
    )

    last_missed_pill = models.CharField(
        verbose_name="When was the last time you missed your study pill?",
        max_length=25,
        choices=MISSED_PILLS,
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Diabetes referral follow-up"
        verbose_name_plural = "Diabetes referral follow-up"
