from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from .model_mixins import CrfModelMixin


class MichiganNeuropathyScreeningInstrument(
    CrfModelMixin,
    edc_models.BaseUuidModel,
):

    """Neuropathy screening tool.

    Uses Michigan Neuropathy Screening Instrument (MNSI).
    """

    numb_legs_feet = models.CharField(
        verbose_name="Are your legs and/or feet numb?",
        max_length=15,
        choices=YES_NO,
    )

    burning_pain_legs_feet = models.CharField(
        verbose_name="Do you ever have any burning pain in your legs and/or feet?",
        max_length=15,
        choices=YES_NO,
    )

    feet_sensitive_touch = models.CharField(
        verbose_name="Are your feet too sensitive to touch?",
        max_length=15,
        choices=YES_NO,
    )

    muscle_cramps_legs_feet = models.CharField(
        verbose_name="Do you get muscle cramps in your legs and/or feet?",
        max_length=15,
        choices=YES_NO,
    )

    prickling_feelings_legs_feet = models.CharField(
        verbose_name="Do you ever have any prickling feelings in your legs or feet?",
        max_length=15,
        choices=YES_NO,
    )

    covers_touch_skin_painful = models.CharField(
        verbose_name="Does it hurt when the bed covers touch your skin?",
        max_length=15,
        choices=YES_NO,
    )

    differentiate_hot_cold_water = models.CharField(
        verbose_name="When you get into the tub or shower, are you able to tell the hot water from the cold water?",
        max_length=15,
        choices=YES_NO,
    )

    open_sore_foot_history = models.CharField(
        verbose_name="Have you ever had an open sore on your foot?",
        max_length=15,
        choices=YES_NO,
    )

    diabetic_neuropathy = models.CharField(
        verbose_name="Has your doctor ever told you that you have diabetic neuropathy?",
        max_length=15,
        choices=YES_NO,
    )

    feel_weak = models.CharField(
        verbose_name="Do you feel weak all over most of the time?",
        max_length=15,
        choices=YES_NO,
    )

    symptoms_worse_night = models.CharField(
        verbose_name="Are your symptoms worse at night?",
        max_length=15,
        choices=YES_NO,
    )

    legs_hurt_when_walk = models.CharField(
        verbose_name="Do your legs hurt when you walk?",
        max_length=15,
        choices=YES_NO,
    )

    sense_feet_when_walk = models.CharField(
        verbose_name="Are you able to sense your feet when you walk?",
        max_length=15,
        choices=YES_NO,
    )

    skin_cracks_open_feet = models.CharField(
        verbose_name="Is the skin on your feet so dry that it cracks open?",
        max_length=15,
        choices=YES_NO,
    )

    amputation = models.CharField(
        verbose_name="Have you ever had an amputation?",
        max_length=15,
        choices=YES_NO,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Michigan Neuropathy Screening Instrument (MNSI)"
        verbose_name_plural = "Michigan Neuropathy Screening Instrument (MNSI)"
