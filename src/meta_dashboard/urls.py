from edc_protocol.research_protocol_config import ResearchProtocolConfig

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
    url_names_key="subject_listboard_url",
    identifier_pattern=ResearchProtocolConfig().subject_identifier_pattern,
)
urlpatterns += ScreeningListboardView.urls(
    namespace=app_name,
    url_names_key="screening_listboard_url",
    identifier_label="screening_identifier",
    identifier_pattern=screening_identifier,
)
urlpatterns += SubjectDashboardView.urls(
    namespace=app_name,
    url_names_key="subject_dashboard_url",
    identifier_pattern=ResearchProtocolConfig().subject_identifier_pattern,
)

urlpatterns += AeListboardView.urls(
    namespace=app_name,
    url_names_key="ae_listboard_url",
    identifier_pattern=ResearchProtocolConfig().subject_identifier_pattern,
)
urlpatterns += DeathReportListboardView.urls(
    namespace=app_name,
    url_names_key="death_report_listboard_url",
    identifier_pattern=ResearchProtocolConfig().subject_identifier_pattern,
)
