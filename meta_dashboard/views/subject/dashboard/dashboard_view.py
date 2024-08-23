from typing import Any

from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.html import format_html
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
        context = super().get_context_data(**kwargs)
        try:
            Endpoints.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            pass
        else:
            url = reverse("meta_reports_admin:meta_reports_glucosesummary_changelist")
            url = f"{url}?q={self.subject_identifier}"
            message = _(
                format_html(
                    f"Subject has reached the protocol endpoint. "
                    f'See <A href="{url}">{GlucoseSummary._meta.verbose_name}</A>'
                )
            )
            self.message_user(message, level=messages.WARNING)
        return context
