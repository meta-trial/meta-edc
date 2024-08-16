from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class UnattendedTwoInRow(QaReportModelMixin, models.Model):

    appt_datetime = models.DateTimeField()

    first = models.CharField(max_length=25)

    second = models.CharField(max_length=25)

    interval_days = models.IntegerField()

    from_now_days = models.IntegerField()

    class Meta:
        managed = False
        db_table = "unattended_two_in_row_view"
        verbose_name = "R120: Unattended appointments: Two in a row"
        verbose_name_plural = "R120: Unattended appointments: Two in a row"
        default_permissions = qa_reports_permissions
