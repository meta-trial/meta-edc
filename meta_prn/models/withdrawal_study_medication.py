# TODO: urine_bhcg form (probably not necessary)
# TODO: if pos, take of study drug and estimate delivery
#  date for the pregnancy outcomes form. See Form 25/26
# from django.db import models
# from edc_action_item.models import ActionModelMixin
# from edc_constants.choices import YES_NO
# from edc_identifier.model_mixins import (
#     NonUniqueSubjectIdentifierFieldMixin,
#     TrackingModelMixin,
# )
# from edc_model import models as edc_models
# from edc_model.models import date_is_future
# from edc_sites.models import SiteModelMixin
# from edc_utils import get_utcnow
#
# from ..choices import WITHDRAWAL_STUDY_MEDICATION_REASONS
# from ..constants import WITHDRAWAL_STUDY_MEDICATION_ACTION
#
#
# class WithdrawalStudyMedication(
#     NonUniqueSubjectIdentifierFieldMixin,
#     SiteModelMixin,
#     ActionModelMixin,
#     TrackingModelMixin,
#     edc_models.BaseUuidModel,
# ):
#
#     action_name = WITHDRAWAL_STUDY_MEDICATION_ACTION
#
#     tracking_identifier_prefix = "WM"
#
#     report_datetime = models.DateTimeField(
#         verbose_name="Report Date and Time", default=get_utcnow
#     )
#
#     stop_date = models.DateField(
#         verbose_name="Date study medication stopped",
#     )
#
#     last_taken_date = models.DateField(
#         verbose_name="Date participant last took study medication",
#     )
#
#     reason = models.CharField(
#         verbose_name="Reason for stopping study medication",
#         max_length=25,
#         choices=WITHDRAWAL_STUDY_MEDICATION_REASONS,
#     )
#
#     permanently_discontinued = models.CharField(
#         verbose_name="Is study medication being permanently discontinued",
#         max_length=15,
#         choices=YES_NO,
#     )
#
#     permanently_discontinued_reason = models.TextField(
#         verbose_name="Reason study medication being permanently discontinued",
#         null=True,
#         blank=True,
#     )
#
#     expected_restart_date = models.DateField(
#         verbose_name="If not permanently discontinued, expected restart date",
#         validators=[date_is_future],
#         null=True,
#         blank=True,
#     )
#
#     class Meta(edc_models.BaseUuidModel.Meta):
#         verbose_name = "Withdrawal of Study Drug"
#         verbose_name_plural = "Withdrawal of Study Drug"
#         # unique_together = ["subject_identifier", "edd"]
