from django.db.models.signals import pre_save
from django.dispatch import receiver
from edc_consent.utils import get_consent_model_cls
from edc_pharmacy.utils import create_prescription
from edc_visit_schedule.constants import DAY1

from meta_edc.meta_version import PHASE_THREE, get_meta_version

from .study_medication import StudyMedication


@receiver(
    pre_save,
    weak=False,
    sender=StudyMedication,
    dispatch_uid="study_medication_on_pre_save",
)
def study_medication_on_pre_save(sender, instance, raw, **kwargs):
    """Create a prescription if one does not exist

    Note: this should not be necessary if consented after meta_consent.signal
          was updated to call `create_prescription`.
    """
    if (
        not raw
        and get_meta_version() == PHASE_THREE
        and instance.subject_visit.visit_code == DAY1
    ):
        subject_consent = get_consent_model_cls().objects.get(
            subject_identifier=instance.subject_visit.subject_identifier,
        )
        create_prescription(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            randomizer_name=get_meta_version(),
            medication_name="Metformin",
        )
