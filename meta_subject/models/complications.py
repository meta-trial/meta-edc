from django.db import models
from edc_constants.choices import NORMAL_ABNORMAL, PRESENT_ABSENT, YES_NO
from edc_model import models as edc_models

from ..choices import FUNDOSCOPY_CHOICES
from ..model_mixins import CrfModelMixin


class Complications(CrfModelMixin, edc_models.BaseUuidModel):
    cataracts = models.CharField(
        verbose_name="Presence of cataracts", max_length=15, choices=YES_NO
    )

    fundoscopy = models.CharField(
        verbose_name="Fundoscopy", max_length=35, choices=FUNDOSCOPY_CHOICES
    )

    achilles_tendon_reflex = models.CharField(
        verbose_name="Achilles tendon reflex", max_length=15, choices=PRESENT_ABSENT
    )

    foot_pin_prick = models.CharField(
        verbose_name="Pin prick testing on foot",
        max_length=15,
        choices=NORMAL_ABNORMAL,
        help_text="Can the patient distinguish between sharp and non-sharp?",
    )

    foot_light_touch = models.CharField(
        verbose_name="Light touch",
        max_length=15,
        choices=NORMAL_ABNORMAL,
        help_text="Can the patient feel light pressure on the dorsum of the foot?",
    )

    temperature_perception = models.CharField(
        verbose_name="Temperature perception",
        max_length=15,
        choices=NORMAL_ABNORMAL,
        help_text=(
            "Can the patient distinguish between temperature on the dorsum of the foot?"
        ),
    )

    dorsalis_pedis_pulse = models.CharField(
        verbose_name="Dorsalis pedis pulse", max_length=15, choices=PRESENT_ABSENT
    )

    posterior_tibial_pulse = models.CharField(
        verbose_name="Posterior tibial pulse", max_length=15, choices=PRESENT_ABSENT
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Presence of Complications"
        verbose_name_plural = "Presence of Complications"
