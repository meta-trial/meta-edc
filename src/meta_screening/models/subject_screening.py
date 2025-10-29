from clinicedc_constants import PENDING, QUESTION_RETIRED
from django.contrib.sites.models import Site
from django.core.validators import RegexValidator
from django.db import models
from django_crypto_fields.fields import EncryptedCharField
from edc_model.models import BaseUuidModel
from edc_screening.model_mixins import ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)
from edc_utils import get_utcnow

from ..model_mixins import (
    CalculatedModelMixin,
    EligibilityModelMixin,
    PartOneFieldsModelMixin,
    PartThreeFieldsModelMixin,
    PartTwoFieldsModelMixin,
)


class SubjectScreeningModelError(Exception):
    pass


class ScreeningIdentifier(BaseScreeningIdentifier):
    template = "S{random_string}"


class SubjectScreening(
    PartOneFieldsModelMixin,
    PartTwoFieldsModelMixin,
    PartThreeFieldsModelMixin,
    EligibilityModelMixin,
    CalculatedModelMixin,
    ScreeningModelMixin,
    BaseUuidModel,
):
    identifier_cls = ScreeningIdentifier
    # consent_definitions = [consent_v1]

    contact_number = EncryptedCharField(
        validators=[RegexValidator(r"^[0-9\-\(\)\ ]+$", message="Enter a valid number")],
        null=True,
        help_text="Provide a contact number if repeating glucose measures (Encryption: RSA)",
    )

    site = models.ForeignKey(Site, on_delete=models.PROTECT, null=True, related_name="+")

    def save(self, *args, **kwargs):
        if self._meta.label_lower == "meta_screening.subjectscreening":
            raise SubjectScreeningModelError("Unable to save. Save via P1-3 proxy models.")
        self.consent_ability = QUESTION_RETIRED
        super().save(*args, **kwargs)

    @property
    def human_readable_identifier(self):
        """Returns a humanized screening identifier."""
        x = self.screening_identifier
        return f"{x[0:4]}-{x[4:]}"

    @property
    def repeat_due_in_days(self):
        if self.repeat_glucose_performed == PENDING and self.ogtt_datetime:
            return (get_utcnow() - self.ogtt_datetime).days
        return 0

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
