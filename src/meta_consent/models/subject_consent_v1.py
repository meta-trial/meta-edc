from edc_consent.managers import ConsentObjectsByCdefManager, CurrentSiteByCdefManager
from edc_model.models import HistoricalRecords

from .subject_consent import SubjectConsent


class SubjectConsentV1(SubjectConsent):
    objects = ConsentObjectsByCdefManager()
    on_site = CurrentSiteByCdefManager()
    history = HistoricalRecords()

    class Meta:
        proxy = True
        verbose_name = "Consent V1"
        verbose_name_plural = "Consent V1"
