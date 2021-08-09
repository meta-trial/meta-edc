from django.db import models
from edc_constants.choices import POS_NEG_NA, YES_NO, YES_NO_NA
from edc_constants.constants import NO, NOT_APPLICABLE

from ..choices import YES_NO_NOT_ELIGIBLE
from ..constants import PREG_YES_NO_NA


class PartTwoFieldsModelMixin(models.Model):

    part_two_report_datetime = models.DateTimeField(
        verbose_name="Part 2 report date and time",
        null=True,
        blank=False,
        help_text="Date and time of report.",
    )

    urine_bhcg_performed = models.CharField(
        verbose_name="Was a Urine or serum βhCG performed?",
        max_length=15,
        choices=PREG_YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="(Pregnancy test)",
    )

    urine_bhcg_value = models.CharField(
        verbose_name="Urine or serum βhCG result",
        max_length=15,
        choices=POS_NEG_NA,
        default=NOT_APPLICABLE,
    )

    urine_bhcg_date = models.DateField(
        verbose_name="Urine or serum βhCG date", blank=True, null=True
    )

    congestive_heart_failure = models.CharField(
        verbose_name=(
            "Does the patient have congestive heart failure "
            "requiring pharmacologic therapy"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    liver_disease = models.CharField(
        verbose_name="Is there clinical evidence of liver disease",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text=(
            "Evidence of chronic liver disease: Jaundice, pruritus, "
            "hepatomegaly, ascites, spider naevi and flapping tremors."
        ),
    )

    alcoholism = models.CharField(
        verbose_name=(
            "Does the patient have any evidence of alcoholism or "
            "acute alcohol intoxication"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text=(
            "Evidence of alcoholism or acute alcohol intoxication: "
            "flushing, amnesia, mental confusion, nausea or vomiting, "
            "slurred speech, dehydration, dry skin and brittle hair."
        ),
    )

    acute_metabolic_acidosis = models.CharField(
        verbose_name=(
            "Does the patient have any signs or symptoms of acute metabolic acidosis"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text="lactic acidosis and/or diabetic ketoacidosis",
    )
    renal_function_condition = models.CharField(
        verbose_name=(
            "Does the patient have any acute condition which can alter renal "
            "function including: dehydration, severe infection or shock"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    tissue_hypoxia_condition = models.CharField(
        verbose_name=(
            "Does the patient have any acute condition which can cause tissue "
            "hypoxia"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text=(
            "Including: decompensated heart failure, respiratory failure, "
            "recent myocardial infarction or shock"
        ),
    )

    acute_condition = models.CharField(
        verbose_name=(
            "Does the patient have any acute condition requiring "
            "immediate hospital care/admission"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    metformin_sensitivity = models.CharField(
        verbose_name=(
            "Does the patient have any known hypersensitivity to metformin "
            "or any excipients associated with its preparation"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text=(
            "For example: Magnesium stearate, sodium "
            "carboxymethylcellulose, hypromellose"
        ),
    )

    # META PHASE_THREE ONLY
    has_dm = models.CharField(
        verbose_name="Is the patient known to have diabetes?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    # META PHASE_THREE ONLY
    on_dm_medication = models.CharField(
        verbose_name="Is the patient known to be taking anti-diabetic medications?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    already_fasted = models.CharField(
        verbose_name="Has the patient come to the clinic today already fasted?",
        max_length=15,
        choices=YES_NO_NOT_ELIGIBLE,
        default=NO,
    )

    advised_to_fast = models.CharField(
        verbose_name=(
            "Has the patient been advised to return fasted for the second "
            "stage of the screening?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    appt_datetime = models.DateTimeField(
        verbose_name="Appointment date for second stage of screening",
        null=True,
        blank=True,
        help_text=(
            "You may use today's date if the patient has already fasted and has "
            "agreed to complete the second stage of screening today"
        ),
    )

    class Meta:
        abstract = True
