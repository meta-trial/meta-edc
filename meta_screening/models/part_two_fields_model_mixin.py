from django.contrib import admin
from django.db import models
from edc_constants.choices import POS_NEG_NA, YES_NO, YES_NO_NA
from edc_constants.constants import NO, NOT_APPLICABLE, YES

from ..choices import YES_NO_NOT_ELIGIBLE, YES_PENDING_NA
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
            "Does the patient have congestive heart failure requiring pharmacologic therapy"
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
            "Does the patient have any evidence of alcoholism or acute alcohol intoxication"
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
            "Does the patient have any acute condition which can cause tissue hypoxia"
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
            "For example: Magnesium stearate, sodium carboxymethylcellulose, hypromellose"
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

    agree_to_p3 = models.CharField(
        verbose_name=(
            "Has the patient agreed to complete/return for the second stage of the screening?"
        ),
        max_length=15,
        choices=YES_NO_NOT_ELIGIBLE,
        default=YES,
        help_text=(
            "If patient is not continuing to the second stage today, advised to "
            "fast and provide a return appointment date below"
        ),
    )

    advised_to_fast = models.CharField(
        verbose_name=(
            "Has the patient been advised to return FASTED for the second "
            "stage of the screening?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="Not applicable if continuing to the second stage today",
    )

    appt_datetime = models.DateTimeField(
        verbose_name="Appointment date for second stage of screening (P3)",
        null=True,
        blank=True,
        help_text="Leave blank if continuing to the second stage today",
    )

    p3_ltfu = models.CharField(
        max_length=15,
        verbose_name="Consider the patient 'lost to screening' for now?",
        choices=YES_PENDING_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Only applicable if the patient missed the appointment for the second stage "
            "of screening (P3), several attempts have been made to contact the patient, "
            "and the patient has not started P3. See above"
        ),
    )

    p3_ltfu_date = models.DateField(
        verbose_name="Date decision made",
        null=True,
        blank=True,
        help_text="Must be after the appointment date for the second stage of screening (P3)",
    )

    p3_ltfu_comment = models.TextField(
        verbose_name="Provide any additional comments on this decision (or leave blank)",
        null=True,
        blank=True,
    )

    @admin.display(description="P3 appointment", ordering="appt_datetime")
    def p3_appt(self):
        return self.appt_datetime

    class Meta:
        abstract = True
