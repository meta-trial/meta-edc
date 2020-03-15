from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from edc_crf.model_mixins import CrfModelMixin
from meta_lists.models import (
    Symptoms,
    ArvRegimens,
    OiProphylaxis,
    DiabetesSymptoms,
    HypertensionMedications,
)
from edc_reportable.units import (
    CELLS_PER_MILLIMETER_CUBED_DISPLAY,
    COPIES_PER_MILLILITER,
)
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField


class PatientHistory(CrfModelMixin, BaseUuidModel):

    symptoms = models.ManyToManyField(
        Symptoms, verbose_name="Do you have any of the following symptoms?"
    )

    other_symptoms = OtherCharField(null=True, blank=True)

    hiv_diagnosis_date = models.DateField(
        verbose_name="When was the diagnosis of HIV made?", null=True, blank=True
    )

    arv_initiation_date = models.DateField(
        verbose_name="Date of start of antiretroviral therapy (ART)",
        null=True,
        blank=True,
    )

    viral_load = models.IntegerField(
        verbose_name="Last viral load",
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        null=True,
        blank=True,
        help_text=COPIES_PER_MILLILITER,
    )

    viral_load_date = models.DateField(
        verbose_name="Date of last viral load", null=True, blank=True
    )

    cd4 = models.IntegerField(
        verbose_name="Last CD4",
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        null=True,
        blank=True,
        help_text=CELLS_PER_MILLIMETER_CUBED_DISPLAY,
    )

    cd4_date = models.DateField(verbose_name="Date of last CD4", null=True, blank=True)

    current_arv_regimen = models.ForeignKey(
        ArvRegimens,
        on_delete=models.PROTECT,
        related_name="current_arv_regimen",
        verbose_name=(
            "Which antiretroviral therapy regimen is the patient currently on?"
        ),
        null=True,
        blank=False,
    )

    other_current_arv_regimen = OtherCharField(null=True, blank=True)

    current_arv_regimen_start_date = models.DateField(
        verbose_name=(
            "When did the patient start this current antiretroviral therapy regimen?"
        ),
        null=True,
        blank=True,
    )

    has_previous_arv_regimen = models.CharField(
        verbose_name="Has the patient been on any previous regimen?",
        max_length=15,
        choices=YES_NO,
    )

    previous_arv_regimen = models.ForeignKey(
        ArvRegimens,
        on_delete=models.PROTECT,
        related_name="previous_arv_regimen",
        verbose_name=(
            "Which antiretroviral therapy regimen was the patient previously on?"
        ),
        null=True,
        blank=True,
    )

    other_previous_arv_regimen = OtherCharField(null=True, blank=True)

    on_oi_prophylaxis = models.CharField(
        verbose_name=(
            "Is the patient on any prophylaxis against opportunistic infections?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    oi_prophylaxis = models.ManyToManyField(
        OiProphylaxis,
        verbose_name="If YES, which prophylaxis is the patient on?",
        blank=True,
    )

    other_oi_prophylaxis = OtherCharField(null=True, blank=True)

    hypertension_diagnosis = models.CharField(
        verbose_name="Has the patient been diagnosed with hypertension?",
        max_length=15,
        choices=YES_NO,
    )

    on_hypertension_treatment = models.CharField(
        verbose_name="Is the patient on treatment for hypertension?",
        max_length=15,
        choices=YES_NO,
    )

    hypertension_treatment = models.ManyToManyField(
        HypertensionMedications,
        verbose_name=(
            "What medications is the patient currently taking for hypertension?"
        ),
        blank=True,
    )

    other_hypertension_treatment = OtherCharField(
        verbose_name=mark_safe("If other medication(s), please specify ..."),
        null=True,
        blank=True,
    )

    taking_statins = models.CharField(
        verbose_name="Is the patient currently taking any statins?",
        max_length=15,
        choices=YES_NO,
    )

    current_smoker = models.CharField(
        verbose_name=mark_safe("Is the patient a <u>current</u> smoker?"),
        max_length=15,
        choices=YES_NO,
    )

    former_smoker = models.CharField(
        verbose_name=mark_safe("Is the patient a <u>previous</u> smoker?"),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    diabetes_symptoms = models.ManyToManyField(
        DiabetesSymptoms,
        verbose_name=mark_safe(
            "In the <u>past year</u>, have you had any of the following symptoms?"
        ),
    )

    other_diabetes_symptoms = OtherCharField(
        verbose_name=mark_safe(
            "If other symptom in the <u>past year</u>, please specify ..."
        ),
        null=True,
        blank=True,
    )

    diabetes_in_family = models.CharField(
        verbose_name=(
            "Has anyone in your immediate family " "ever been diagnosed with diabetes?"
        ),
        max_length=15,
        choices=YES_NO,
        help_text="Immediate family is parents, siblings, and children",
    )

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Patient History"
        verbose_name_plural = "Patient History"
