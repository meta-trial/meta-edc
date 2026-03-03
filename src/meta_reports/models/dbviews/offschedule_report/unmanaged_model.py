from clinicedc_constants import NULL_STRING
from django.db import models
from django_db_views.db_view import DBView
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions

from .view_definition import get_view_definition


class OffscheduleReport(QaReportModelMixin, DBView):
    source = models.CharField(max_length=35, default=NULL_STRING)

    visit_schedule_name = models.CharField(max_length=150, default=NULL_STRING)

    schedule_name = models.CharField(max_length=150, default=NULL_STRING)

    onschedule_model = models.CharField(max_length=150, default=NULL_STRING)

    onschedule_datetime = models.DateTimeField(null=True)

    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "meta_reports_offschedulereportview"
        verbose_name = "Subjects awaiting `Off Schedule` report"
        verbose_name_plural = "Subjects awaiting `Off Schedule` report"
        default_permissions = qa_reports_permissions
