from edc_qareports.model_mixins import qa_reports_permissions

from .endpoints import Endpoints


class EndpointsProxy(Endpoints):
    class Meta:
        proxy = True
        verbose_name = "Endpoints (DM): All"
        verbose_name_plural = "Endpoints (DM): All"
        default_permissions = qa_reports_permissions
