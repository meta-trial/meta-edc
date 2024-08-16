from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class PatientHistoryMissingBaselineCd4(QaReportModelMixin, models.Model):

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField()

    cd4 = models.IntegerField(verbose_name="Last CD4")

    cd4_date = models.DateField(verbose_name="Date of last CD4")

    user_created = models.CharField(max_length=25)

    user_modified = models.CharField(max_length=25)

    modified = models.DateTimeField()

    class Meta:
        verbose_name = "Patient History: Missing Baseline Cd4"
        verbose_name_plural = "Missing Baseline Cd4"
        managed = False
        db_table = "patient_history_missing_baseline_cd4_view"
        default_permissions = qa_reports_permissions
