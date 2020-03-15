from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_crf.model_mixins import CrfModelMixin
from edc_model.models import BaseUuidModel
from edc_model_fields.fields.other_charfield import OtherCharField
from meta_lists.models import NonAdherenceReasons

from ..choices import MISSED_PILLS


class MedicationAdherence(CrfModelMixin, BaseUuidModel):

    visual_score_slider = models.CharField(
        verbose_name="Visual score", max_length=3, help_text="%"
    )

    visual_score_confirmed = models.IntegerField(
        verbose_name=mark_safe(
            "<B><font color='orange'>Interviewer</font></B>: "
            "please confirm the score indicated from above."
        ),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="%",
    )

    last_missed_pill = models.CharField(
        verbose_name="When was the last time you missed your study pill?",
        max_length=25,
        choices=MISSED_PILLS,
    )

    pill_count = models.IntegerField(verbose_name="Number of pills left in the bottle")

    missed_pill_reason = models.ManyToManyField(
        NonAdherenceReasons, verbose_name="Reasons for missing study pills", blank=True
    )

    other_missed_pill_reason = OtherCharField()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Medication Adherence"
        verbose_name_plural = "Medication Adherence"
