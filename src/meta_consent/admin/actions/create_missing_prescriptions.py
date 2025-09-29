from django.contrib import admin, messages
from edc_pharmacy.exceptions import PrescriptionAlreadyExists
from edc_pharmacy.models import Medication
from edc_pharmacy.prescribe import create_prescription

from meta_consent.models import SubjectConsent
from meta_edc.meta_version import get_meta_version
from meta_pharmacy.constants import METFORMIN


@admin.action(permissions=["view"], description="Create missing METFORMIN prescription")
def create_missing_metformin_rx(modeladmin, request, queryset):  # noqa: ARG001
    medication = Medication.objects.get(name=METFORMIN)
    total = queryset.count()
    subject_identifiers = queryset.values_list("subject_identifier", flat=True)
    subject_consents_wo_rx = SubjectConsent.objects.filter(
        subject_identifier__in=subject_identifiers
    )
    created = 0
    exist = 0
    for instance in subject_consents_wo_rx:
        try:
            create_prescription(
                subject_identifier=instance.subject_identifier,
                report_datetime=instance.consent_datetime,
                randomizer_name=get_meta_version(),
                medication_names=[medication.name],
                site_id=instance.site.id,
            )
        except PrescriptionAlreadyExists:
            exist += 1
        else:
            created += 1
    messages.success(
        request,
        f"Created {created}/{total} missing {medication.display_name} prescriptions. "
        f"Got {exist}/{total} prescriptions already exist",
    )
