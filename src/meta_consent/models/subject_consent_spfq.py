from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_crypto_fields.fields import EncryptedCharField
from edc_consent.field_mixins import (
    ReviewFieldsMixin,
)
from edc_consent.managers import ConsentObjectsManager
from edc_constants.choices import GENDER
from edc_constants.constants import NULL_STRING
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.model_mixins import SiteModelMixin

from .model_mixins import SearchSlugModelMixin


class SubjectConsentSpfq(
    SiteModelMixin,
    ReviewFieldsMixin,
    SearchSlugModelMixin,
    BaseUuidModel,
):
    """A model completed by the user that captures the ICF for SPFQ."""

    subject_identifier = models.CharField(
        verbose_name=_("Subject identifier"), max_length=50, unique=True
    )

    initials = EncryptedCharField(
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{2,3}$",
                message="Ensure initials consist of letters only in upper case, no spaces.",
            )
        ],
        default=NULL_STRING,
    )

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER,
        max_length=1,
    )

    consent_datetime = models.DateTimeField(
        verbose_name=_("Consent datetime"), default=timezone.now
    )

    report_datetime = models.DateTimeField(null=True, editable=False)

    language = models.CharField(
        verbose_name=_("Language of consent"),
        max_length=25,
        choices=settings.LANGUAGES,
        help_text=_(
            "The language used for the consent process will "
            "also be used during data collection."
        ),
    )

    model_name = models.CharField(
        verbose_name="model",
        max_length=50,
        help_text=(
            "label_lower of this model class. Will be different if "
            "instance has been added/edited via a proxy model"
        ),
        default=NULL_STRING,
        editable=False,
    )

    version = models.CharField(
        verbose_name="Consent version",
        max_length=10,
        default="1.0",
        help_text="See 'consent definition' for consent versions by period.",
        editable=False,
    )

    on_site = CurrentSiteManager()

    objects = ConsentObjectsManager()

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.subject_identifier} V{self.version}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.model_name = self._meta.label_lower
        self.report_datetime = self.consent_datetime
        super().save(*args, **kwargs)

    def natural_key(self):
        return self.subject_identifier, self.version

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Subject Consent for SPFQ"
        verbose_name_plural = "Subject Consents for SPFQ"
