from django.db import models
from django_db_views.db_view import DBView
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions

from .view_definition import get_view_definition


class MissingScreeningOgtt(QaReportModelMixin, DBView):
    screening_datetime = models.DateTimeField(null=True)

    fbg_datetime = models.DateTimeField(null=True)

    fbg_value = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    ogtt_value = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    fbg2_value = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    ogtt2_value = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    fbg2_datetime = models.DateTimeField(null=True)

    ogtt2_datetime = models.DateTimeField(null=True)

    repeated = models.CharField(
        default="", max_length=25, help_text="repeat_glucose_performed"
    )

    p3_ltfu = models.CharField(default="", max_length=25)

    consented = models.BooleanField(null=True)

    original_id = models.UUIDField(null=True)

    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "missing_screening_ogtt_view"
        verbose_name = "Screening: Missing OGTT"
        verbose_name_plural = "Screening: Missing OGTT"
        default_permissions = qa_reports_permissions
