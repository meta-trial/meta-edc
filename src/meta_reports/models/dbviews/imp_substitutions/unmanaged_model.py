from clinicedc_constants import NOT_EVALUATED
from django.db import models
from django_db_views.db_view import DBView
from edc_constants.choices import YES_NO_NOT_EVALUATED
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions

from .view_definition import get_view_definition


class ImpSubstitutions(QaReportModelMixin, DBView):
    original_id = models.UUIDField(null=True)

    sid = models.IntegerField(verbose_name="Original SID", null=True)

    dispensed_sid = models.IntegerField(verbose_name="Dispensed SID", null=True)

    arm_match = models.CharField(
        max_length=15,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
    )

    report_datetime = models.DateTimeField(null=True)

    allocated_datetime = models.DateTimeField(null=True)

    user_created = models.CharField(max_length=25)

    user_modified = models.CharField(max_length=25)

    modified = models.DateTimeField(null=True)

    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "imp_subjectitutions_view"
        verbose_name = "IMP Substitutions"
        verbose_name_plural = "IMP Substitutions"
        default_permissions = qa_reports_permissions
