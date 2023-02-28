from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from edc_adverse_event.models import CauseOfDeath
from edc_constants.choices import YES_NO
from edc_model_fields.fields import OtherCharField

from ..choices import DEATH_LOCATIONS, INFORMANT_RELATIONSHIP


class DeathReportModelMixin(models.Model):
    death_location = models.CharField(
        verbose_name="Where did the participant die?",
        max_length=50,
        choices=DEATH_LOCATIONS,
    )

    # TODO: if hospital of clinic, require, else NA
    hospital_name = models.CharField(
        verbose_name=(
            "If death occurred at hospital / clinic, please give name of the facility"
        ),
        max_length=150,
        null=True,
        blank=True,
    )

    informant_contact = EncryptedTextField(null=True, blank=True)

    informant_relationship = models.CharField(
        max_length=50,
        choices=INFORMANT_RELATIONSHIP,
        verbose_name="Informants relationship to the participant?",
    )

    other_informant_relationship = OtherCharField()

    death_certificate = models.CharField(
        verbose_name="Is a death certificate is available?",
        max_length=15,
        choices=YES_NO,
    )

    secondary_cause_of_death = models.ForeignKey(
        CauseOfDeath,
        on_delete=models.PROTECT,
        related_name="secondary_cause_of_death",
        verbose_name="Secondary cause of death",
        help_text=(
            "Secondary cause of death in the opinion of the " "local study doctor and local PI"
        ),
    )

    secondary_cause_of_death_other = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='If "Other" above, please specify',
    )

    class Meta:
        abstract = True
