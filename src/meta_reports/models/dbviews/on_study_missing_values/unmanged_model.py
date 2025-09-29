from django_db_views.db_view import DBView
from edc_qareports.model_mixins import (
    OnStudyMissingValuesModelMixin,
    QaReportModelMixin,
    qa_reports_permissions,
)

from .view_definition import get_view_definition


class OnStudyMissingValues(OnStudyMissingValuesModelMixin, QaReportModelMixin, DBView):
    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "onstudy_missing_values_view"
        verbose_name = "Missing values for on-study patient"
        verbose_name_plural = "Missing values for on-study patients"
        default_permissions = qa_reports_permissions
