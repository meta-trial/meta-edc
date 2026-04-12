from clinicedc_constants import NO, YES
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.urls import reverse
from edc_data_manager.auth_objects import DATA_MANAGER_ROLE
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_offstudy.constants import WITHDRAWAL
from edc_registration.models import RegisteredSubject
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.admin.list_filters import SitesForDataManagerListFilter

from meta_prn.models import EndOfStudy

from ..admin_site import meta_spfq_admin
from ..models import (
    SpfqForWithdrawal,
    SpfqForWithdrawalList,
    SubjectConsentSpfqForWithdrawal,
)


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
                subject_identifier__in=SpfqForWithdrawal.objects.values_list(
                    "subject_identifier", flat=True
                )
            )
        if self.value() == NO:
            return queryset.exclude(
                subject_identifier__in=SpfqForWithdrawal.objects.values_list(
                    "subject_identifier", flat=True
                )
            )
        return queryset


@admin.register(SpfqForWithdrawalList, site=meta_spfq_admin)
class SpfqForWithdrawalListAdmin(
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
        "gender",
        "age_in_years",
        "uploaded_document",
    )

    list_filter = (CompletedSpfqListFilter, SitesForDataManagerListFilter)

    search_fields = ("subject_identifier",)

    readonly_fields = (
        "sid",
        "subject_identifier",
        "site",
        "gender",
        "age_in_years",
    )

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        subject_identifiers = qs.values_list("subject_identifier", flat=True)
        for eos_obj in EndOfStudy.objects.filter(offstudy_reason__name=WITHDRAWAL).exclude(
            subject_identifier__in=subject_identifiers
        ):
            if eos_obj.subject_identifier not in self.model.objects.values_list(
                "subject_identifier", flat=True
            ):
                new_obj = self.model()
                new_obj.subject_identifier = eos_obj.subject_identifier
                new_obj.site = eos_obj.site
                new_obj.save()
        return super().get_queryset(request)

    @admin.display(description="Upload")
    def uploaded_document(self, obj=None) -> str | None:
        try:
            spfq_for_withdrawal = SpfqForWithdrawal.objects.get(
                registered_subject__subject_identifier=obj.subject_identifier
            )
        except ObjectDoesNotExist:
            return None
        return spfq_for_withdrawal.upload

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
            consent_obj = SubjectConsentSpfqForWithdrawal.objects.get(
                subject_identifier=obj.subject_identifier
            )
        except ObjectDoesNotExist:
            url = reverse("meta_spfq_admin:meta_spfq_subjectconsentspfqforwithdrawal_add")
            title = "Add Consent"
            color = "#ffc107"
        else:
            url = reverse(
                "meta_spfq_admin:meta_spfq_subjectconsentspfqforwithdrawal_change",
                args=[consent_obj.id],
            )
            title = "Consented"
            color = "#198754"

        if consent_obj:
            try:
                spfq_obj = SpfqForWithdrawal.objects.get(
                    registered_subject__subject_identifier=obj.subject_identifier
                )
            except ObjectDoesNotExist:
                spfq_url = reverse("meta_spfq_admin:meta_spfq_spfqforwithdrawal_add")
                spfq_url = f"{spfq_url}"
                spfq_title = "Add SPFQ for withdrawal"
                spfq_color = "#ffc107"
            else:
                spfq_url = reverse(
                    "meta_spfq_admin:meta_spfq_spfqforwithdrawal_change",
                    args=[spfq_obj.id],
                )
                spfq_title = "SPFQ for withdrawal"
                spfq_color = "#198754"
        else:
            try:
                refusal_obj = SpfqForWithdrawal.objects.get(
                    registered_subject__subject_identifier=obj.subject_identifier
                )
            except ObjectDoesNotExist:
                refusal_url = reverse("meta_spfq_admin:meta_spfq_spfqforwithdrawalrefusal_add")
                refusal_url = f"{refusal_url}"
                refusal_title = "Add Refusal"
                refusal_color = "#ffc107"
            else:
                refusal_url = reverse(
                    "meta_spfq_admin:meta_spfq_spfqforwithdrawalrefusal_change",
                    args=[refusal_obj.id],
                )
                refusal_title = "Refused"
                refusal_color = "#dc3545"

        rs_obj = RegisteredSubject.objects.get(subject_identifier=obj.subject_identifier)
        next_querystring = (
            "meta_spfq_admin:meta_spfq_spfqforwithdrawallist_changelist,"
            f"subject_identifier,registered_subject"
            f"&subject_identifier={obj.subject_identifier}"
            f"&registered_subject={rs_obj.id}"
        )
        context = dict(
            url=url,
            subject_identifier=obj.subject_identifier,
            title=title,
            next=next_querystring,
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
