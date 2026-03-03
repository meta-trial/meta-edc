from clinicedc_constants import NULL_STRING
from django.db import models
from django_db_views.db_view import DBView
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions

from .view_definition import get_view_definition


class EosReport(QaReportModelMixin, DBView):
    offschedule_datetime = models.DateTimeField(null=True)

    source = models.CharField(max_length=35, default=NULL_STRING)

    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "meta_reports_eosreportview"
        verbose_name = "Subjects off schedule awaiting `End of Study` report"
        verbose_name_plural = "Subjects off schedule awaiting `End of Study` report"
        default_permissions = qa_reports_permissions
