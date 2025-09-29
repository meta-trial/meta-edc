from django.db import models
from django_pandas.managers import DataFrameManager
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class LastImpRefill(QaReportModelMixin, models.Model):
    reference_date = models.DateField(null=True)

    imp_visit_code = models.FloatField(null=True)

    imp_visit_date = models.DateField(null=True)

    next_visit_code = models.FloatField(null=True)

    next_appt_date = models.DateField(null=True)

    visit_code = models.CharField(max_length=15, default="")

    visit_code_sequence = models.IntegerField(null=True)

    days_since = models.IntegerField(null=True)

    days_until = models.IntegerField(null=True)

    objects = DataFrameManager()

    def recreate_db_view(self, **kwargs):
        raise NotImplementedError()

    class Meta(QaReportModelMixin.Meta):  # noqa: DJ012
        verbose_name = "Last IMP Refill"
        verbose_name_plural = "Last IMP Refills"
        default_permissions = qa_reports_permissions
