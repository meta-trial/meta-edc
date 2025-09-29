from django.db import models
from django_db_views.db_view import DBView
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions

from .view_definition import get_view_definition


class PatientHistoryMissingBaselineCd4(QaReportModelMixin, DBView):
    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField()

    cd4 = models.IntegerField(verbose_name="Last CD4")

    cd4_date = models.DateField(verbose_name="Date of last CD4")

    user_created = models.CharField(max_length=25)

    user_modified = models.CharField(max_length=25)

    modified = models.DateTimeField()

    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "patient_history_missing_baseline_cd4_view"
        verbose_name = "Patient History: Missing Baseline Cd4"
        verbose_name_plural = "Missing Baseline Cd4"
        default_permissions = qa_reports_permissions
