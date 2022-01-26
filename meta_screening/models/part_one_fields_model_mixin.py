from django.db import models
from django.utils.safestring import mark_safe
from django_crypto_fields.fields import EncryptedCharField
from edc_constants.choices import SELECTION_METHOD, YES_NO, YES_NO_NA, YESDEFAULT_NO
from edc_constants.constants import YES

from ..choices import ETHNICITY
from ..constants import PREG_YES_NO_NA


class PartOneFieldsModelMixin(models.Model):

    screening_consent = models.CharField(
        verbose_name=(
            "Has the subject given his/her verbal consent "
            "to be screened for the META trial?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    selection_method = models.CharField(
        verbose_name="How was the patient selected from the outpatients CTC?",
        max_length=25,
        choices=SELECTION_METHOD,
    )

    meta_phase_two = models.CharField(
        verbose_name="Was the subject enrolled in the META Phase 2 trial?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    hospital_identifier = EncryptedCharField(unique=True, blank=False)

    ethnicity = models.CharField(
        max_length=15, choices=ETHNICITY, help_text="Used for eGFR calculation"
    )

    hiv_pos = models.CharField(
        verbose_name="Is the patient HIV positive", max_length=15, choices=YES_NO
    )

    art_six_months = models.CharField(
        verbose_name=(
            "Has the patient been on anti-retroviral therapy for at least 6 months"
        ),
        max_length=15,
        choices=YES_NO_NA,
    )

    on_rx_stable = models.CharField(
        verbose_name="Is the patient considered to be stable on treatment ",
        max_length=15,
        choices=YES_NO_NA,
        help_text="in regular attendance for care",
    )

    lives_nearby = models.CharField(
        verbose_name=(
            "Is the patient living within the catchment population of the facility"
        ),
        max_length=15,
        choices=YES_NO,
    )

    # META PHASE_TWO ONLY
    staying_nearby_6 = models.CharField(
        verbose_name=(
            "Is the patient planning to remain in the catchment area "
            "for at least 6 months"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    # META PHASE_THREE ONLY
    staying_nearby_12 = models.CharField(
        verbose_name=(
            "Is the patient planning to remain in the catchment area "
            "for at least 12 months"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    pregnant = models.CharField(
        verbose_name="Is the patient pregnant?", max_length=15, choices=PREG_YES_NO_NA
    )

    continue_part_two = models.CharField(
        verbose_name=mark_safe(
            "Continue with <U>part two</U> of the screening process?"
        ),
        max_length=15,
        choices=YESDEFAULT_NO,
        default=YES,
        help_text=mark_safe(
            "<B>Important</B>: This response will be be automatically "
            "set to YES if:<BR><BR>"
            "- the participant meets the eligibility criteria for part one, or;<BR><BR>"
            "- the eligibility criteria for part two is already complete.<BR>"
        ),
    )

    class Meta:
        abstract = True
