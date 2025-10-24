from typing import Any

from django.apps import apps as django_apps
from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from edc_subject_dashboard.views import SubjectDashboardView

from meta_reports.models import Endpoints, GlucoseSummary


class DashboardView(SubjectDashboardView):
    consent_model = "meta_consent.subjectconsentv1"
    navbar_selected_item = "consented_subject"
    visit_model = "meta_subject.subjectvisit"
    history_button_label = _("Audit")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add message if subject reaches DM Endpoint."""
        kwargs.update(subject_consent_v1_ext=self.subject_consent_v1_ext)
        try:
            Endpoints.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            pass
        else:
            url = reverse("meta_reports_admin:meta_reports_glucosesummary_changelist")
            url = mark_safe(f"{url}?q={self.subject_identifier}")  # noqa: S308
            message = format_html(
                '{text} <A href="{url}">{verbose_name}</A>',
                text=_("Subject has reached the protocol endpoint. See "),
                url=url,
                verbose_name=GlucoseSummary._meta.verbose_name,
            )
            self.message_user(message, level=messages.WARNING)
        return super().get_context_data(**kwargs)

    @property
    def subject_consent_v1_ext(self):
        model_cls = django_apps.get_model("meta_consent.subjectconsentv1ext")
        try:
            obj = model_cls.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            obj = None
        return obj
