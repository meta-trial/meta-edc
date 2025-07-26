from django.db import models
from edc_constants.choices import NORMAL_ABNORMAL_NOEXAM
from edc_model.models import BaseUuidModel

from ..choices import (
    FUNDOSCOPY_CHOICES,
    PRESENT_ABSENT_NOEXAM,
    PRESENT_ABSENT_NOEXAM_NDS,
    YES_NO_NO_EXAM,
)
from ..model_mixins import CrfModelMixin


class ComplicationsGlycemia(CrfModelMixin, BaseUuidModel):
    """Not used"""

    # eye examination
    cataracts = models.CharField(
        verbose_name="Presence of cataracts", max_length=15, choices=YES_NO_NO_EXAM
    )

    fundoscopy = models.CharField(
        verbose_name="Fundoscopy", max_length=35, choices=FUNDOSCOPY_CHOICES
    )

    # foot examination
    foot_skin_condition = models.CharField(
        verbose_name="Is the skin of the foot intact and in good condition?",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    foot_fungal_infection = models.CharField(
        verbose_name="Is there any fungal infection on the foot?",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    foot_sores = models.CharField(
        verbose_name="Are there any foot sores?",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    foot_callouses = models.CharField(
        verbose_name="Are there any callouses on the foot?",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    # Peripheral pulses and reflexes

    dp_pulse = models.CharField(
        verbose_name="Dorsalis pedis pulse",
        max_length=15,
        choices=PRESENT_ABSENT_NOEXAM,
    )

    pt_pulse = models.CharField(
        verbose_name="Posterior tibial pulse",
        max_length=15,
        choices=PRESENT_ABSENT_NOEXAM,
    )

    at_reflex = models.CharField(
        verbose_name="Achilles tendon reflex",
        max_length=15,
        choices=PRESENT_ABSENT_NOEXAM,
    )

    # Neuropathy Disability Score (NDS)
    nds_vpt_left = models.CharField(
        verbose_name="Vibration perception threshold (left)",
        max_length=15,
        choices=NORMAL_ABNORMAL_NOEXAM,
        help_text=(
            "128-Hz tuning fork; apex of big toe. "
            "Normal: can distinguish vibrating/Not vibrating"
        ),
    )

    nds_vpt_right = models.CharField(
        verbose_name="Vibration perception threshold (right)",
        max_length=15,
        choices=NORMAL_ABNORMAL_NOEXAM,
        help_text=(
            "128-Hz tuning fork; apex of big toe. "
            "Normal: can distinguish vibrating/Not vibrating"
        ),
    )

    nds_tp_left = models.CharField(
        verbose_name="Temperature perception on dorsum of foot (left)",
        max_length=15,
        choices=NORMAL_ABNORMAL_NOEXAM,
        help_text="Use tuning fork with beaker of ice/warm water",
    )

    nds_tp_right = models.CharField(
        verbose_name="Temperature perception on dorsum of foot (right)",
        max_length=15,
        choices=NORMAL_ABNORMAL_NOEXAM,
        help_text="Use tuning fork with beaker of ice/warm water",
    )

    nds_pp_left = models.CharField(
        verbose_name="Pin-Prick (left)",
        max_length=15,
        choices=NORMAL_ABNORMAL_NOEXAM,
        help_text="Use tuning fork with beaker of ice/warm water",
    )

    nds_pp_right = models.CharField(
        verbose_name="Pin-Prick (right)",
        max_length=15,
        choices=NORMAL_ABNORMAL_NOEXAM,
        help_text="Use tuning fork with beaker of ice/warm water",
    )

    nds_achilles_reflex_left = models.CharField(
        verbose_name="Achilles reflex (left)",
        max_length=30,
        choices=PRESENT_ABSENT_NOEXAM_NDS,
    )

    nds_achilles_reflex_right = models.CharField(
        verbose_name="Achilles reflex (right)",
        max_length=30,
        choices=PRESENT_ABSENT_NOEXAM_NDS,
    )

    # 10-g monofilament test
    first_metatarsal_left = models.CharField(
        verbose_name="First metatarsal (left)",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    first_metatarsal_right = models.CharField(
        verbose_name="First metatarsal (right)",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    third_metatarsal_left = models.CharField(
        verbose_name="Third metatarsal (left)",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    third_metatarsal_right = models.CharField(
        verbose_name="Third metatarsal (right)",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    fifth_metatarsal_left = models.CharField(
        verbose_name="Fifth metatarsal (left)",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    fifth_metatarsal_right = models.CharField(
        verbose_name="Fifth metatarsal (right)",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    plantar_surface_left = models.CharField(
        verbose_name="Plantar surface of distal hallux (left)",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    plantar_surface_right = models.CharField(
        verbose_name="Plantar surface of distal hallux (right)",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    # Diabetic Neuropathy Symptom Score

    dns_walking = models.CharField(
        verbose_name="Are you experiencing unsteadiness in walking?",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    dns_burning = models.CharField(
        verbose_name="Do you have burning, aching pain or tenderness in your legs or feet?",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    dns_tingling = models.CharField(
        verbose_name="Do you have prickling or tingling sensation in your legs or feet?",
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    dns_numbness = models.CharField(
        verbose_name=(
            "Are you experiencing any numbness or loss of feeling in your legs or feet?"
        ),
        max_length=15,
        choices=YES_NO_NO_EXAM,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Complications (Raised Glycemia)"
        verbose_name_plural = "Complications (Raised Glycemia)"
