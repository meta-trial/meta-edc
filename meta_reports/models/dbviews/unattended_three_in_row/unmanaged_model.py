from django.db import models
from django_db_views.db_view import DBView
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions

from .view_definition import get_view_definition


class UnattendedThreeInRow(QaReportModelMixin, DBView):

    appt_datetime = models.DateTimeField()

    first_value = models.CharField(verbose_name="First", max_length=25)

    second_value = models.CharField(verbose_name="Second", max_length=25)

    third_value = models.CharField(verbose_name="Third", max_length=25)

    interval_days = models.IntegerField()

    from_now_days = models.IntegerField()

    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "unattended_three_in_row_view"
        verbose_name = "R100: Unattended appointments: Three in a row"
        verbose_name_plural = "R100: Unattended appointments: Three in a row"
        default_permissions = qa_reports_permissions
