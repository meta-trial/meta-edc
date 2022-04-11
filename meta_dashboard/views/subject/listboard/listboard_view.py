import re

from django.db.models import Q
from edc_dashboard.view_mixins import (
    EdcViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
)
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin
from edc_subject_model_wrappers import SubjectConsentModelWrapper


class ListboardView(
    EdcViewMixin,
    NavbarViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
    BaseListboardView,
):

    listboard_template = "subject_listboard_template"
    listboard_url = "subject_listboard_url"
    listboard_panel_style = "success"
    listboard_fa_icon = "far fa-user-circle"
    listboard_model = "meta_consent.subjectconsent"
    listboard_view_permission_codename = "edc_dashboard.view_subject_listboard"

    model_wrapper_cls = SubjectConsentModelWrapper
    navbar_selected_item = "consented_subject"
    search_form_url = "subject_listboard_url"

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get("subject_identifier"):
            options.update({"subject_identifier": kwargs.get("subject_identifier")})
        return options

    def extra_search_options(self, search_term):
        q_objects = []
        if re.match(r"^[A-Za-z\-]+$", search_term):
            q_objects.append(Q(initials__exact=search_term.upper()))
            q_objects.append(Q(first_name__exact=search_term.upper()))
            q_objects.append(
                Q(screening_identifier__icontains=search_term.replace("-", "").upper())
            )
            q_objects.append(Q(subject_identifier__icontains=search_term))
        if re.match(r"^[0-9]+$", search_term):
            q_objects.append(Q(identity__exact=search_term))
        return q_objects
