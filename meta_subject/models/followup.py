from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_crf.model_mixins import CrfModelMixin
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField
from meta_lists.models import Symptoms, ArvRegimens

from ..choices import FOLLOWUP_REASONS, GRADE34_CHOICES


class Followup(CrfModelMixin, BaseUuidModel):

    # 3
    followup_reason = models.CharField(
        verbose_name="Why have you come to the clinic today",
        max_length=25,
        choices=FOLLOWUP_REASONS,
    )

    # 4a
    symptoms = models.ManyToManyField(
        Symptoms,
        related_name="symptoms",
        verbose_name=(
            "Since your last appointment have you experienced "
            "any of the following symptoms"
        ),
        help_text="either at this hospital or at a different clinic",
    )

    # 4b
    symptoms_sought_care = models.ManyToManyField(
        Symptoms,
        related_name="symptoms_sought_care",
        verbose_name="Did you seek care from any health worker for these symptoms",
    )

    # 4a
    symptoms_g3 = models.ManyToManyField(
        Symptoms,
        related_name="symptoms_g3",
        verbose_name="For these symptoms, were any grade 3 events",
        help_text=(
            "Refer to DAIDS toxicity table. "
            "Please complete Serious Adverse Event form"
        ),
    )

    # 4a
    symptoms_g4 = models.ManyToManyField(
        Symptoms,
        related_name="symptoms_g4",
        verbose_name="For these symptoms, were any grade 4 events",
        help_text=(
            "Refer to DAIDS toxicity table. "
            "Please complete Serious Adverse Event form"
        ),
    )

    # 4c
    symptoms_detail = models.TextField(
        verbose_name="Please provide details on any of the symptoms above.",
        null=True,
        blank=True,
    )

    # 5a
    attended_clinic = models.CharField(
        verbose_name=(
            "Since your last visit did you attend any other clinic or hospital "
            "for care for any reason"
        ),
        max_length=25,
        choices=YES_NO,
        help_text=(
            "Includes other routine appointments, e.g. BP check or family planning"
        ),
    )

    # 5b
    admitted_hospital = models.CharField(
        verbose_name="If YES, were you admitted to hospital?",
        max_length=25,
        choices=YES_NO,
    )

    # 5c
    attended_clinic_detail = models.TextField(
        verbose_name=(
            "If YES, attend other clinic or hospital, "
            "please provide details of this visit"
        ),
        help_text=(
            "If patient was given a referral letter or "
            "discharge summary record details here"
        ),
        null=True,
        blank=True,
    )

    # 5d
    prescribed_medication = models.CharField(
        verbose_name=(
            "Were you prescribed any other medication at "
            "this clinic or hospital visit?"
        ),
        max_length=25,
        choices=YES_NO,
    )

    # 5d
    prescribed_medication_detail = models.TextField(
        verbose_name=(
            "If YES, prescribed any other medication, "
            "please provide details of this visit"
        ),
        null=True,
        blank=True,
    )

    # 5d
    attended_clinic_sae = models.CharField(
        verbose_name=(
            "Does the visit described in 5b constitute a Serious Adverse Event"
        ),
        max_length=25,
        choices=YES_NO,
        help_text="If YES, submit a Serious Adverse Event Form",
    )

    # 6a
    any_other_problems = models.CharField(
        verbose_name=(
            "Since your last visit have you experienced any other "
            "medical or health problems not listed above"
        ),
        max_length=25,
        choices=YES_NO,
    )

    # 6a
    any_other_problems_detail = models.TextField(
        verbose_name=("If YES, please provide details"), null=True, blank=True
    )

    any_other_problems_sae = models.CharField(
        verbose_name="Does this event constitute an Adverse Event?",
        max_length=25,
        choices=YES_NO,
        help_text="If YES, grade 3 or 4 submit Serious Adverse Event form",
    )

    any_other_problems_sae = models.CharField(
        verbose_name="If YES, what grade?",
        max_length=25,
        choices=GRADE34_CHOICES,
        default=NOT_APPLICABLE,
        help_text="If YES, grade 3 or 4, submit Serious Adverse Event form",
    )

    # 7a
    art_change = models.CharField(
        verbose_name=(
            "Since your last visit has there been any change in your HIV medication?"
        ),
        max_length=25,
        choices=YES_NO,
    )

    # 7b
    art_change_reason = models.TextField(
        verbose_name=("If YES, please provide reason for change"), null=True, blank=True
    )

    # 7c
    art_new_regimen = models.ManyToManyField(
        ArvRegimens,
        verbose_name="Please indicate new regimen",
        related_name="art_new_regimen",
    )

    art_new_regimen_other = OtherCharField()

    abdominal_tenderness = models.CharField(
        verbose_name="Abdominal tenderness", max_length=25, choices=YES_NO
    )

    enlarged_liver = models.CharField(
        verbose_name="Enlarged liver", max_length=25, choices=YES_NO
    )

    jaundice = models.CharField(verbose_name="Jaundice", max_length=25, choices=YES_NO)

    comment = models.TextField(
        verbose_name=(
            "Comment on the clinical course, any other symptoms present, "
            "assessment and management plan"
        )
    )

    lactic_acidosis = models.CharField(
        verbose_name="Do you think this patient has lactic acidosis?",
        max_length=25,
        choices=YES_NO,
        help_text=(
            "Classical signs of lactic acidosis include: abdominal or stomach "
            "discomfort, decreased appetite, diarrhoea, fast or shallow breathing, "
            "a general feeling of discomfort, muscle pain or cramping; and "
            "unusual sleepiness, fatigue, or weakness."
        ),
    )

    hepatomegaly = models.CharField(
        verbose_name="Do you think this patient has hepatomegaly with steatosis?",
        max_length=25,
        choices=YES_NO,
        help_text=(
            "This condition often does not have any clinical signs and symptoms, "
            "it may present with an enlarge liver on examination, and symptoms "
            "of fatigue and right upper abdominal pain. The risk of developing "
            "this condition is higher in patients who are obese and who have "
            "type 2 diabetes or metabolic syndrome"
        ),
    )

    referral = models.CharField(
        verbose_name="Is patient being referred", max_length=25, choices=YES_NO
    )

    referral_reason = models.TextField(
        verbose_name="If YES, what is the reason for referral", null=True, blank=True
    )

    referral_reason = models.TextField(
        verbose_name="If YES, where are they being referred to",
        null=True,
        blank=True,
        help_text=(
            "Note: remind participant that admission or discharge information "
            "will be needed at the next follow up visit."
        ),
    )

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Clinic follow up: Examination"
        verbose_name_plural = "Clinic follow up: Examination"
