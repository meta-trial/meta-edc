from django.contrib.admin import SimpleListFilter

from ..constants import NOT_SUBMITTED, SUBMITTED
from ..models import EndOfStudy


class EosListFilter(SimpleListFilter):
    title = "End of Study"
    parameter_name = "eos"
    model_cls = EndOfStudy

    def lookups(self, request, model_admin):  # noqa: ARG002
        return (
            (SUBMITTED, "Submitted"),
            (NOT_SUBMITTED, "Not submitted"),
        )

    def queryset(self, request, queryset):  # noqa: ARG002
        qs = None
        if self.value():
            subject_identifiers = EndOfStudy.objects.values_list("subject_identifier").all()
            if self.value() == SUBMITTED:
                qs = queryset.filter(subject_identifier__in=subject_identifiers)
            elif self.value() == NOT_SUBMITTED:
                qs = queryset.exclude(subject_identifier__in=subject_identifiers)
        return qs
