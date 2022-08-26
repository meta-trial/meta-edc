from django.core.validators import RegexValidator
from django_crypto_fields.fields import EncryptedCharField
from edc_constants.constants import QUESTION_RETIRED
from edc_model.models import BaseUuidModel
from edc_screening.model_mixins import ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)

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

    contact_number = EncryptedCharField(
        validators=[RegexValidator(r"^[0-9\-\(\)\ ]+$", message="Enter a valid number")],
        null=True,
        help_text="Provide a contact number if repeating glucose measures (Encryption: RSA)",
    )

    def save(self, *args, **kwargs):
        if self._meta.label_lower == "meta_screening.subjectscreening":
            raise SubjectScreeningModelError("Unable to save. Save via P1-3 proxy models.")
        self.consent_ability = QUESTION_RETIRED
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
