from clinicedc_constants import NO, YES
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from edc_data_manager.auth_objects import DATA_MANAGER_ROLE
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.admin.list_filters import SitesForDataManagerListFilter

from ..admin_site import meta_spfq_admin
from ..models import Spfq, SpfqList, SpfqRefusal, SubjectConsentSpfq


class CompletedSpfqListFilter(SimpleListFilter):
    title = "Completed SPQF"
    parameter_name = "completed_spqf"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return (
            (YES, YES),
            (NO, NO),
        )

    def queryset(self, request, queryset):  # noqa: ARG002
        if self.value() == YES:
            return queryset.filter(
                subject_identifier__in=Spfq.objects.values_list(
                    "subject_identifier", flat=True
                )
            )
        if self.value() == NO:
            return queryset.exclude(
                subject_identifier__in=Spfq.objects.values_list(
                    "subject_identifier", flat=True
                )
            )
        return queryset


@admin.register(SpfqList, site=meta_spfq_admin)
class SpfqListAdmin(
    ModelAdminSubjectDashboardMixin,
    SiteModelAdminMixin,
    SimpleHistoryAdmin,
):
    ordering = ("sid",)

    list_display = (
        "sid",
        "subject_identifier",
        "dashboard",
        "consent_button",
        "last_visit_code",
        "last_appt_datetime",
        "gender",
        "age_in_years",
        "weight_bin",
        "date_generated",
        "filename",
    )

    list_filter = (CompletedSpfqListFilter, SitesForDataManagerListFilter)

    search_fields = ("subject_identifier",)

    readonly_fields = (
        "sid",
        "subject_identifier",
        "site",
        "last_visit_code",
        "last_appt_datetime",
        "gender",
        "age_in_years",
        "weight_bin",
        "date_generated",
        "filename",
    )

    @admin.display(description="Documents")
    def consent_button(self, obj=None) -> str:
        consent_obj = None
        spfq_obj = None
        spfq_url = ""
        spfq_title = ""
        spfq_color = ""
        refusal_obj = None
        refusal_url = ""
        refusal_title = ""
        refusal_color = ""
        try:
            consent_obj = SubjectConsentSpfq.objects.get(
                subject_identifier=obj.subject_identifier
            )
        except ObjectDoesNotExist:
            url = reverse("meta_spfq_admin:meta_spfq_subjectconsentspfq_add")
            title = "Add Consent"
            color = "#ffc107"
        else:
            url = reverse(
                "meta_spfq_admin:meta_spfq_subjectconsentspfq_change",
                args=[consent_obj.id],
            )
            title = "Consented"
            color = "#198754"

        if consent_obj:
            try:
                spfq_obj = Spfq.objects.get(subject_identifier=obj.subject_identifier)
            except ObjectDoesNotExist:
                spfq_url = reverse("meta_spfq_admin:meta_spfq_spfq_add")
                spfq_url = f"{spfq_url}"
                spfq_title = "Add SPFQ"
                spfq_color = "#ffc107"
            else:
                spfq_url = reverse(
                    "meta_spfq_admin:meta_spfq_spfq_change",
                    args=[spfq_obj.id],
                )
                spfq_title = "SPFQ"
                spfq_color = "#198754"
        else:
            try:
                refusal_obj = SpfqRefusal.objects.get(
                    subject_identifier=obj.subject_identifier
                )
            except ObjectDoesNotExist:
                refusal_url = reverse("meta_spfq_admin:meta_spfq_spfqrefusal_add")
                refusal_url = f"{refusal_url}"
                refusal_title = "Add Refusal"
                refusal_color = "#ffc107"
            else:
                refusal_url = reverse(
                    "meta_spfq_admin:meta_spfq_spfqrefusal_change",
                    args=[refusal_obj.id],
                )
                refusal_title = "Refused"
                refusal_color = "#dc3545"

        context = dict(
            url=url,
            subject_identifier=obj.subject_identifier,
            title=title,
            next=(
                "meta_spfq_admin:meta_spfq_spfqlist_changelist,"
                f"subject_identifier&subject_identifier={obj.subject_identifier}"
            ),
            color=color,
            consent_obj=consent_obj,
            spfq_obj=spfq_obj,
            spfq_url=spfq_url,
            spfq_title=spfq_title,
            spfq_color=spfq_color,
            refusal_obj=refusal_obj,
            refusal_url=refusal_url,
            refusal_title=refusal_title,
            refusal_color=refusal_color,
        )
        return render_to_string("meta_spfq/documents_button.html", context=context)

    def get_view_only_site_ids_for_user(self, request) -> list[int]:
        if request.user.userprofile.roles.filter(name=DATA_MANAGER_ROLE).exists():
            return [
                s.id for s in request.user.userprofile.sites.all() if s.id != request.site.id
            ]
        return super().get_view_only_site_ids_for_user(request)

    def user_may_view_other_sites(self, request) -> bool:  # noqa: ARG002
        return True
