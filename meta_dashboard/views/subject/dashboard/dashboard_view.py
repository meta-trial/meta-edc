from django.utils.translation import gettext_lazy as _
from edc_subject_dashboard.views import SubjectDashboardView


class DashboardView(SubjectDashboardView):
    consent_model = "meta_consent.subjectconsentv1"
    navbar_selected_item = "consented_subject"
    visit_model = "meta_subject.subjectvisit"
    history_button_label = _("Audit")
