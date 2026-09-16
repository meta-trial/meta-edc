from clinicedc_constants import NO, YES
from clinicedc_constants.choices import YES_NO
from django.contrib import admin
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from ..constants import REQUIRES_REVIEW


class FinalAeClassificationSetListFilter(admin.SimpleListFilter):
    title = _("Final AE classification set")
    parameter_name = "final_ae_classification_set"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return YES_NO

    def queryset(self, request, queryset):  # noqa: ARG002
        if self.value() == YES:
            return queryset.filter(final_ae_classification__isnull=False)
        if self.value() == NO:
            return queryset.filter(final_ae_classification__isnull=True)
        return queryset


class HasAeTmgListFilter(admin.SimpleListFilter):
    title = _("Has AE TMG")
    parameter_name = "has_aetmg"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return YES_NO

    def queryset(self, request, queryset):  # noqa: ARG002
        if self.value() == YES:
            return queryset.filter(ae_tmg__isnull=False)
        if self.value() == NO:
            return queryset.filter(ae_tmg__isnull=True)
        return queryset


class NeedsReviewListFilter(admin.SimpleListFilter):
    """Records waiting on a reviewer.

    Either the sources do not agree and nobody has settled the record,
    or the sources have moved since somebody did.
    """

    title = _("Needs review")
    parameter_name = "needs_review"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return YES_NO

    def queryset(self, request, queryset):  # noqa: ARG002
        if self.value() not in [YES, NO]:
            return queryset
        # a null TMG side on both is a match, which `=` alone would miss
        investigator_holds = Q(
            resolved_investigator_ae_classification__isnull=True,
            investigator_ae_classification__isnull=True,
        ) | Q(resolved_investigator_ae_classification=F("investigator_ae_classification"))
        unsettled = Q(review_status=REQUIRES_REVIEW) & ~Q(conflict_resolved=YES)
        stale = Q(conflict_resolved=YES) & (
            ~Q(resolved_ae_classification=F("ae_classification")) | ~investigator_holds
        )
        if self.value() == YES:
            return queryset.filter(unsettled | stale)
        return queryset.exclude(unsettled | stale)
