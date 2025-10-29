from clinicedc_constants import NULL_STRING
from django.db import models
from django_db_views.db_view import DBView
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions

from .view_definition import get_view_definition


class GlucoseSummary(QaReportModelMixin, DBView):
    fbg_value = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    fbg_units = models.CharField(max_length=15, default=NULL_STRING)

    fbg_datetime = models.DateTimeField(null=True)

    ogtt_value = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    ogtt_units = models.CharField(max_length=15, default=NULL_STRING)

    ogtt_datetime = models.DateTimeField(null=True)

    fasted = models.CharField(max_length=15, default=NULL_STRING)

    fasting_duration_delta = models.DurationField(
        verbose_name="Fasting duration (hrs)", null=True
    )

    report_datetime = models.DateTimeField(null=True)

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField()

    appointment_id = models.UUIDField(null=True)

    offstudy_datetime = models.DateTimeField(null=True)

    source = models.CharField(max_length=35, default=NULL_STRING)

    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "meta_reports_glucosesummaryview"
        verbose_name = "Glucose Summary"
        verbose_name_plural = "Glucose Summary"
        default_permissions = qa_reports_permissions
