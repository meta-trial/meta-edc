from urllib.parse import parse_qs, urlsplit

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_constants.constants import YES
from edc_lab.admin import (
    RequisitionAdminMixin,
    requisition_fieldset,
    requisition_identifier_fieldset,
    requisition_status_fieldset,
    requisition_verify_fieldset,
)

from ..admin_site import meta_subject_admin
from ..forms import SubjectRequisitionForm
from ..models import SubjectRequisition
from .modeladmin import CrfModelAdmin


@admin.register(SubjectRequisition, site=meta_subject_admin)
class SubjectRequisitionAdmin(RequisitionAdminMixin, CrfModelAdmin):

    form = SubjectRequisitionForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "requisition_datetime", "panel")}),
        requisition_fieldset,
        requisition_status_fieldset,
        requisition_identifier_fieldset,
        requisition_verify_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "is_drawn": admin.VERTICAL,
        "reason_not_drawn": admin.VERTICAL,
        "item_type": admin.VERTICAL,
    }

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        path = urlsplit(request.META.get("HTTP_REFERER")).path
        query = urlsplit(request.META.get("HTTP_REFERER")).query
        if "bloodresult" in path:
            attrs = parse_qs(query)
            try:
                subject_visit = attrs.get("subject_visit")[0]
            except (TypeError, IndexError):
                pass
            else:
                queryset = queryset.filter(subject_visit=subject_visit, is_drawn=YES)
        return queryset, use_distinct
