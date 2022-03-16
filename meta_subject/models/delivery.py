# TODO: urine_bhcg form (probably not necessary)
# TODO: if pos, take of study drug and estimate delivery date for the pregnancy outcomes form. See Form 25/26
from django.apps import apps as django_apps
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from edc_constants.choices import YES_NO
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models
from edc_model.models import datetime_not_future
from edc_model_fields.fields import OtherCharField
from edc_protocol.validators import datetime_not_before_study_start
from edc_utils import get_utcnow

from meta_ae.choices import INFORMANT_RELATIONSHIP

from ..choices import DELIVERY_LOCATIONS, MATERNAL_OUTCOMES
from ..constants import DELIVERY_ACTION


class DeliveryError(Exception):
    pass


class Delivery(
    CrfWithActionModelMixin,
    edc_models.BaseUuidModel,
):
    """form 25"""

    action_name = DELIVERY_ACTION

    tracking_identifier_prefix = "DL"

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    informant_is_patient = models.CharField(
        verbose_name="Was this information from study participant?",
        max_length=5,
        choices=YES_NO,
    )

    informant_contact = EncryptedTextField(
        verbose_name=(
            "If information not from study participant, please give "
            "the name and contact details of the informant."
        ),
        null=True,
        blank=True,
    )

    informant_relation = models.CharField(
        verbose_name="Informants relationship to the participant?",
        max_length=25,
        choices=INFORMANT_RELATIONSHIP,
        null=True,
        blank=True,
    )

    informant_relation_other = OtherCharField()

    delivery_datetime = models.DateTimeField(
        verbose_name="Date and time of delivery :",
        help_text="If TIME unknown, estimate",
        validators=[
            datetime_not_future,
            datetime_not_before_study_start,
        ],
    )

    delivery_time_estimated = models.CharField(
        verbose_name="Is the delivery TIME estimated?", max_length=3, choices=YES_NO
    )

    delivery_location = models.CharField(
        verbose_name="Where did the delivery occur?",
        max_length=25,
        choices=DELIVERY_LOCATIONS,
    )

    delivery_location_other = OtherCharField()

    delivery_location_name = models.CharField(
        verbose_name="If delivery occurred at a `hospital` or `clinic`, please give name of the facility",
        max_length=150,
        null=True,
        blank=True,
    )

    delivery_ga = models.IntegerField(
        verbose_name="Gestational age at delivery",
        validators=[MinValueValidator(1), MaxValueValidator(45)],
    )

    maternal_outcome = models.CharField(
        verbose_name="What was the maternal outcome of the pregnancy?",
        max_length=50,
        choices=MATERNAL_OUTCOMES,
    )

    gm_treated = models.CharField(
        verbose_name="Was the participant treated for gestational diabetes?",
        max_length=5,
        choices=YES_NO,
    )

    fetal_outcome_count = models.IntegerField(
        verbose_name="Number of births / fetal / neonatal outcomes",
        help_text="Each to be reported individually below",
    )

    def save(self, *args, **kwargs):
        pregnancy_notification_model_cls = django_apps.get_model(
            "meta_prn.pregnancynotification"
        )
        if (
            not self.id
            and not pregnancy_notification_model_cls.objects.filter(
                subject_identifier=self.subject_identifier,
                delivered=False,
            ).exists()
        ):
            raise DeliveryError(
                f"Invalid. A {pregnancy_notification_model_cls._meta.verbose_name} cannot be found. "
                "Perhaps catch this in the form."
            )
        super().save(*args, **kwargs)

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Delivery"
        verbose_name_plural = "Delivery"
        unique_together = ["subject_visit", "delivery_datetime"]
