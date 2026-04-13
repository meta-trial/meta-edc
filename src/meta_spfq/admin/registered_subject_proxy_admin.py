from django.contrib import admin
from django.db.models import QuerySet
from edc_offstudy.constants import WITHDRAWAL
from edc_registration.admin import RegisteredSubjectAdmin as BaseRegisteredSubjectAdmin

from meta_prn.models import EndOfStudy

from ..admin_site import meta_spfq_admin
from ..models import RegisteredSubjectProxy


@admin.register(RegisteredSubjectProxy, site=meta_spfq_admin)
class RegisteredSubjectProxyAdmin(BaseRegisteredSubjectAdmin):
    """Registered again for the autocomplete field"""

    fieldsets = (
        (
            "Subject",
            {
                "fields": (
                    "subject_identifier",
                    "initials",
                    "dob",
                    "gender",
                )
            },
        ),
    )

    list_display = (
        "subject_identifier",
        "initials",
        "dob",
        "gender",
    )
    search_fields = ("subject_identifier",)

    readonly_fields = ("subject_identifier",)

    radio_fields = {"gender": admin.HORIZONTAL}  # noqa: RUF012

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        subject_identifiers = EndOfStudy.objects.values_list(
            "subject_identifier", flat=True
        ).filter(offstudy_reason__name=WITHDRAWAL)
        return qs.filter(subject_identifier__in=subject_identifiers)
