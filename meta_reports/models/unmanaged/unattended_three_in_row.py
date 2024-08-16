from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class UnattendedThreeInRow(QaReportModelMixin, models.Model):

    appt_datetime = models.DateTimeField()

    first = models.CharField(max_length=25)

    second = models.CharField(max_length=25)

    third = models.CharField(max_length=25)

    interval_days = models.IntegerField()

    from_now_days = models.IntegerField()

    class Meta:
        managed = False
        db_table = "unattended_three_in_row_view"
        verbose_name = "R100: Unattended appointments: Three in a row"
        verbose_name_plural = "R100: Unattended appointments: Three in a row"
        default_permissions = qa_reports_permissions
