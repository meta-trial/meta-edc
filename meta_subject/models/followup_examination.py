from django.db import models
from django.db.models import PROTECT
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_crf.crf_status_model_mixin import CrfStatusModelMixin
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models
from edc_model_fields.fields import OtherCharField

from meta_lists.models import ArvRegimens, Symptoms

from ..choices import GRADE34_CHOICES
from ..constants import FOLLOWUP_EXAMINATION_ACTION


class FollowupExamination(
    CrfStatusModelMixin, CrfWithActionModelMixin, edc_models.BaseUuidModel
):

    action_name = FOLLOWUP_EXAMINATION_ACTION

    tracking_identifier_prefix = "FU"

    action_identifier = models.CharField(max_length=50, unique=True, null=True)

    tracking_identifier = models.CharField(max_length=30, unique=True, null=True)

    # 4a
    symptoms = models.ManyToManyField(
        Symptoms,
        related_name="symptoms",
        verbose_name=(
            "Since the participant's last appointment have they experienced "
            "any of the following symptoms"
        ),
        help_text="either at this hospital or at a different clinic",
    )

    # 4b
    symptoms_sought_care = models.ManyToManyField(
        Symptoms,
        related_name="symptoms_sought_care",
        verbose_name="Did they seek care from any health worker for these symptoms",
    )

    # 4a
    symptoms_g3 = models.ManyToManyField(
        Symptoms,
        related_name="symptoms_g3",
        verbose_name="For these symptoms, were any grade 3 events",
        help_text=(
            "Refer to DAIDS toxicity table. " "Please complete Serious Adverse Event form"
        ),
    )
    symptoms_g3_detail = models.TextField(
        verbose_name="Please provide details on any of the Grade 3 symptoms above.",
        null=True,
        blank=True,
    )

    # 4a
    symptoms_g4 = models.ManyToManyField(
        Symptoms,
        related_name="symptoms_g4",
        verbose_name="For these symptoms, were any grade 4 events",
        help_text=(
            "Refer to DAIDS toxicity table. " "Please complete Serious Adverse Event form"
        ),
    )
    symptoms_g4_detail = models.TextField(
        verbose_name="Please provide details on any of the Grade 4 symptoms above.",
        null=True,
        blank=True,
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
            "Since the participant's last visit did they attend any other clinic or hospital "
            "for care for any reason"
        ),
        max_length=25,
        choices=YES_NO,
        help_text=("Includes other routine appointments, e.g. BP check or family planning"),
    )

    # 5b
    admitted_hospital = models.CharField(
        verbose_name="If YES, were they admitted to hospital?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    # 5c
    attended_clinic_detail = models.TextField(
        verbose_name=(
            "If YES, attend other clinic or hospital, " "please provide details of this event"
        ),
        help_text=(
            "If the participant was given a referral letter or "
            "discharge summary record details here"
        ),
        null=True,
        blank=True,
    )

    attended_clinic_sae = models.CharField(
        verbose_name=mark_safe("Does the event constitute a <u>Serious Adverse Event</u>"),
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If YES, submit a <u>Serious Adverse Event</u> Form",
    )

    # 5d
    prescribed_medication = models.CharField(
        verbose_name=(
            "Was the participant prescribed any other medication at "
            "this clinic or hospital visit?"
        ),
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    # 5d
    prescribed_medication_detail = models.TextField(
        verbose_name=(
            "If YES, prescribed any other medication, " "please provide details of this visit"
        ),
        null=True,
        blank=True,
    )

    # TODO: Add diagnoses m2m with other inseatd of any_other_problems

    # 6a
    any_other_problems = models.CharField(
        verbose_name=(
            "Since your last visit has the participant experienced any other "
            "medical or health problems NOT listed above"
        ),
        max_length=25,
        choices=YES_NO,
    )

    # 6a
    any_other_problems_detail = models.TextField(
        verbose_name="If YES, please provide details of the event",
        null=True,
        blank=True,
    )

    any_other_problems_sae = models.CharField(
        verbose_name="Does this event constitute an Adverse Event?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    any_other_problems_sae_grade = models.CharField(
        verbose_name="If YES, what grade?",
        choices=GRADE34_CHOICES,
        max_length=25,
        default=NOT_APPLICABLE,
        help_text="If YES, grade 3 or 4, submit Serious Adverse Event form",
    )

    # 7a
    art_change = models.CharField(
        verbose_name=(
            "Since the participant's last visit has there "
            "been any change in their HIV medication?"
        ),
        max_length=25,
        choices=YES_NO,
    )

    # 7b
    art_change_reason = models.TextField(
        verbose_name="If YES, please provide reason for change", null=True, blank=True
    )

    # 7c
    art_new_regimen = models.ForeignKey(
        ArvRegimens,
        on_delete=PROTECT,
        verbose_name="Please indicate new regimen",
        related_name="art_new_regimen",
        null=True,
        blank=True,
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
        verbose_name="Do you think the participant has lactic acidosis?",
        max_length=25,
        choices=YES_NO,
        help_text=(
            "Submit SAE form. Classical signs of lactic acidosis include: abdominal "
            "or stomach discomfort, decreased appetite, diarrhoea, fast or shallow "
            "breathing, a general feeling of discomfort, muscle pain or cramping; and "
            "unusual sleepiness, fatigue, or weakness."
        ),
    )

    hepatomegaly = models.CharField(
        verbose_name="Do you think the participant has hepatomegaly with steatosis?",
        max_length=25,
        choices=YES_NO,
        help_text=(
            "Submit SAE form. This condition often does not have any clinical "
            "signs and symptoms, it may present with an enlarge liver on examination, "
            "and symptoms of fatigue and right upper abdominal pain. The risk of "
            "developing this condition is higher in patients who are obese and who have "
            "type 2 diabetes or metabolic syndrome"
        ),
    )

    referral = models.CharField(
        verbose_name="Is the participant being referred", max_length=25, choices=YES_NO
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

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinic follow up: Examination"
        verbose_name_plural = "Clinic follow up: Examination"
