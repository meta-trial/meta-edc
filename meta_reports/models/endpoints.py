from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class Endpoints(QaReportModelMixin, models.Model):

    visit_code = models.IntegerField(null=True)

    fasting = models.CharField(max_length=10, null=True)

    fbg_datetime = models.DateTimeField(null=True)

    fbg_value = models.FloatField(null=True)

    ogtt_value = models.FloatField(null=True)

    endpoint_label = models.CharField(max_length=250, null=True)

    baseline_datetime = models.DateTimeField(null=True)

    offstudy_datetime = models.DateTimeField(null=True)

    offstudy_reason = models.CharField(max_length=250, null=True)

    class Meta(QaReportModelMixin.Meta):
        verbose_name = "Endpoints (DM)"
        verbose_name_plural = "Endpoints (DM)"
        default_permissions = qa_reports_permissions
