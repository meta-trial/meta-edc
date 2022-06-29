from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model_fields.fields import OtherCharField

from meta_lists.models import DiabetesSymptoms, HypertensionMedications, Symptoms
from meta_subject.choices import DYSLIPIDAEMIA_RX_CHOICES

from ..model_mixins import ArvHistoryModelMixin, CrfModelMixin


class PatientHistory(ArvHistoryModelMixin, CrfModelMixin, edc_models.BaseUuidModel):

    symptoms = models.ManyToManyField(
        Symptoms, verbose_name="Do you have any of the following symptoms?"
    )

    other_symptoms = OtherCharField(null=True, blank=True)

    htn_diagnosis = models.CharField(
        verbose_name="Has the patient been diagnosed with hypertension?",
        max_length=15,
        choices=YES_NO,
    )

    on_htn_treatment = models.CharField(
        verbose_name="Is the patient on treatment for hypertension?",
        max_length=15,
        choices=YES_NO_NA,
    )

    htn_treatment = models.ManyToManyField(
        HypertensionMedications,
        verbose_name=("What medications is the patient currently taking for hypertension?"),
        blank=True,
    )

    other_htn_treatment = OtherCharField(
        verbose_name=mark_safe("If other medication(s), please specify ..."),
        null=True,
        blank=True,
    )

    taking_statins = models.CharField(
        verbose_name="Is the patient currently taking any statins?",
        max_length=15,
        choices=YES_NO,
    )

    # PHASE_THREE_ONLY
    dyslipidaemia_diagnosis = models.CharField(
        verbose_name="Has the patient been diagnosed with dyslipidaemia?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    # PHASE_THREE_ONLY
    on_dyslipidaemia_treatment = models.CharField(
        verbose_name="Is the patient on treatment for dyslipidaemia?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    # PHASE_THREE_ONLY
    dyslipidaemia_rx = models.CharField(
        verbose_name="What medication is the patient currently taking for dyslipidaemia?",
        max_length=25,
        choices=DYSLIPIDAEMIA_RX_CHOICES,
        default=NOT_APPLICABLE,
    )

    # PHASE_THREE_ONLY
    other_dyslipidaemia_rx = models.CharField(
        verbose_name="What medication is the patient currently taking for dyslipidaemia?",
        max_length=50,
        null=True,
        blank=True,
    )

    # PHASE_THREE_ONLY
    concomitant_conditions = models.TextField(
        verbose_name="Does the patient have any other conditions not mentioned above?",
        max_length=250,
        null=True,
        blank=True,
    )
    # PHASE_THREE_ONLY
    concomitant_medications = models.TextField(
        verbose_name="Is the patient taking any concomitant medications?",
        max_length=250,
        null=True,
        blank=True,
    )

    # PHASE_THREE_ONLY
    previous_arv_regimen_start_date = models.DateField(
        verbose_name=(
            "When did the patient start this previous antiretroviral therapy regimen?"
        ),
        null=True,
        blank=True,
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

    dm_symptoms = models.ManyToManyField(
        DiabetesSymptoms,
        verbose_name=mark_safe(
            "In the <u>past year</u>, have you had any of the following symptoms?"
        ),
    )

    other_dm_symptoms = OtherCharField(
        verbose_name=mark_safe("If other symptom in the <u>past year</u>, please specify ..."),
        null=True,
        blank=True,
    )

    dm_in_family = models.CharField(
        verbose_name=(
            "Has anyone in your immediate family " "ever been diagnosed with diabetes?"
        ),
        max_length=15,
        choices=YES_NO,
        help_text="Immediate family is parents, siblings, and children",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Patient History"
        verbose_name_plural = "Patient History"
