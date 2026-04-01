from clinicedc_constants import NULL_STRING
from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class Endpoints(QaReportModelMixin, models.Model):
    """A QA report model updated using an admin
    action or manually.
    """

    visit_code = models.DecimalField(max_digits=6, decimal_places=1, null=True)

    fasting = models.CharField(max_length=10, default=NULL_STRING)

    fasted_hrs = models.DecimalField(null=True, max_digits=10, decimal_places=1)

    fbg_date = models.DateField(null=True)

    fbg_value = models.FloatField(null=True)

    ogtt_value = models.FloatField(null=True)

    endpoint_label = models.CharField(max_length=250, default=NULL_STRING)

    referral_date = models.DateField(null=True)

    referral_id = models.UUIDField(null=True)

    baseline_date = models.DateField(null=True)

    offstudy_date = models.DateField(null=True)

    offstudy_reason = models.CharField(max_length=250, default=NULL_STRING)

    def __str__(self):
        return f"{self.subject_identifier} {self.visit_code} {self.endpoint_label}"

    class Meta(QaReportModelMixin.Meta):  # noqa: DJ012
        verbose_name = "Endpoints (DM)"
        verbose_name_plural = "Endpoints (DM)"
        default_permissions = qa_reports_permissions
