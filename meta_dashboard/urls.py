from edc_protocol import Protocol

from .patterns import screening_identifier
from .views import (
    AeListboardView,
    DeathReportListboardView,
    ScreeningListboardView,
    SubjectDashboardView,
    SubjectListboardView,
)

app_name = "meta_dashboard"

urlpatterns = SubjectListboardView.urls(
    namespace=app_name,
    label="subject_listboard",
    identifier_pattern=Protocol().subject_identifier_pattern,
)
urlpatterns += ScreeningListboardView.urls(
    namespace=app_name,
    label="screening_listboard",
    identifier_label="screening_identifier",
    identifier_pattern=screening_identifier,
)
urlpatterns += SubjectDashboardView.urls(
    namespace=app_name,
    label="subject_dashboard",
    identifier_pattern=Protocol().subject_identifier_pattern,
)

urlpatterns += AeListboardView.urls(
    namespace=app_name,
    label="ae_listboard",
    identifier_pattern=Protocol().subject_identifier_pattern,
)
urlpatterns += DeathReportListboardView.urls(
    namespace=app_name,
    label="death_report_listboard",
    identifier_pattern=Protocol().subject_identifier_pattern,
)
