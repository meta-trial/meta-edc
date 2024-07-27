from django.db import models
from edc_qareports.models import QaReportModelMixin


class Endpoints(QaReportModelMixin, models.Model):

    visit_code = models.IntegerField()

    fasting = models.CharField(max_length=10)

    fbg_datetime = models.DateTimeField()

    fbg_value = models.FloatField()

    ogtt_value = models.FloatField()

    endpoint_label = models.CharField(max_length=25)

    offstudy_datetime = models.DateTimeField(null=True)

    offstudy_reason = models.CharField(max_length=250, null=True)

    class Meta:
        managed = False
        db_table = "unattended_three_in_row2_view"
        verbose_name = "R110: Unattended appointments: Three in a row (with missed)"
        verbose_name_plural = "R110: Unattended appointments: Three in a row (with missed)"
