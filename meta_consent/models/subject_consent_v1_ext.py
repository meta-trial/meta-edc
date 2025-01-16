from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_consent.field_mixins import ReviewFieldsMixin
from edc_consent.model_mixins import ConsentExtensionModelMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin

from ..constants import CONSENT_V1_EXTENSION_ACTION
from .subject_consent_v1 import SubjectConsentV1


class SubjectConsentV1Ext(
    ConsentExtensionModelMixin,
    SiteModelMixin,
    ActionModelMixin,
    ReviewFieldsMixin,
    BaseUuidModel,
):
    """A consent extension to allow a participant to extend followup
    up to 48 months, or not.
    """

    subject_consent = models.ForeignKey(SubjectConsentV1, on_delete=models.PROTECT)

    action_name = CONSENT_V1_EXTENSION_ACTION

    class Meta(
        ConsentExtensionModelMixin.Meta,
        SiteModelMixin.Meta,
        ActionModelMixin.Meta,
        BaseUuidModel.Meta,
    ):
        verbose_name = "Consent V1 Extension"
        verbose_name_plural = "Consent V1 Extension"
