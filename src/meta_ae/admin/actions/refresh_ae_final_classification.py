from django.contrib import admin, messages

from meta_ae.backfill import backfill_ae_final_classifications
from meta_ae.models import AeInitial

MAX_SUBJECTS_LISTED = 10


@admin.action(permissions=["change"], description="Refresh from the source reports")
def refresh_ae_final_classification(modeladmin, request, queryset):  # noqa: ARG001
    """The admin face of `backfill_ae_final_classification --update-copies`.

    Refreshes the copied columns and `review_status` on the selected
    records, and `final_ae_classification` where the reviewer has not
    settled the record. Records they have settled keep their
    classification, and are named where the sources have moved since.
    """
    qs = AeInitial.objects.filter(id__in=queryset.values_list("ae_initial_id", flat=True))
    result = backfill_ae_final_classifications(qs, update_copies=True)
    messages.success(
        request,
        f"Refreshed {len(result.updated)}/{result.total} AE Final Classification "
        f"record(s) from their source reports. "
        f"{result.skipped} already current.",
    )
    if result.discrepancies:
        subject_identifiers = [obj.subject_identifier for obj in result.discrepancies]
        listed = ", ".join(subject_identifiers[:MAX_SUBJECTS_LISTED])
        if len(subject_identifiers) > MAX_SUBJECTS_LISTED:
            listed = f"{listed} and {len(subject_identifiers) - MAX_SUBJECTS_LISTED} more"
        messages.warning(
            request,
            f"Left {len(result.discrepancies)} resolved record(s) unchanged. The "
            f"source reports have changed since these were resolved, so the final "
            f"classification on them needs another look: {listed}.",
        )
