from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class UnattendedThreeInRow2(QaReportModelMixin, models.Model):

    first = models.CharField(max_length=25)

    second = models.CharField(max_length=25)

    third = models.CharField(max_length=25)

    interval_days = models.IntegerField()

    from_now_days = models.IntegerField()

    missed_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "unattended_three_in_row2_view"
        verbose_name = "R110: Unattended appointments: Three in a row (with missed)"
        verbose_name_plural = "R110: Unattended appointments: Three in a row (with missed)"
        default_permissions = qa_reports_permissions
