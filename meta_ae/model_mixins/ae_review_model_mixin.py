from django.conf import settings
from django.db import models
from edc_adverse_event.choices import STUDY_DRUG_RELATIONSHIP
from edc_adverse_event.models import AeClassification
from edc_constants.choices import YES_NO
from edc_model import models as edc_models
from edc_model.validators import datetime_not_future
from edc_utils import get_utcnow

from ..choices import AE_TYPE


class AeReviewModelMixin(models.Model):
    ae_initial = models.ForeignKey(
        f"{settings.ADVERSE_EVENT_APP_LABEL}.aeinitial", on_delete=models.PROTECT
    )

    report_datetime = models.DateTimeField(
        verbose_name="Report date and time",
        validators=[datetime_not_future],
        default=get_utcnow,
    )

    clinical_review_datetime = models.DateTimeField(
        blank=True,
        null=True,
        validators=[datetime_not_future],
        verbose_name="Date and time of clinical review: ",
    )

    ae_classification = models.ForeignKey(
        AeClassification,
        on_delete=models.PROTECT,
        verbose_name="Adverse Event (AE) Classification",
        null=True,
        blank=False,
    )

    ae_classification_other = edc_models.OtherCharField(max_length=250, blank=True, null=True)

    ae_type = models.CharField(verbose_name="Type of event", max_length=25, choices=AE_TYPE)

    study_drug_relation = models.CharField(
        verbose_name="Relationship to study drug:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
        null=True,
    )

    ae_expected = models.CharField(
        verbose_name="Based on the protocol, do you believe this event is expected?",
        max_length=25,
        choices=YES_NO,
        null=True,
    )

    ae_action_required = models.CharField(
        verbose_name="If unexpected, do you believe further action is required?",
        max_length=25,
        choices=YES_NO,
        null=True,
    )

    investigator_comments = models.TextField(
        blank=True, null=True, verbose_name="This Clinical Reviewer's comments:"
    )

    original_report_agreed = models.CharField(
        verbose_name="Does this Clinical Reviewer agree with the original AE report?",
        max_length=15,
        choices=YES_NO,
        blank=False,
        null=True,
        help_text="If No, explain in the narrative below",
    )

    narrative = models.TextField(verbose_name="Narrative", blank=True, null=True)

    officials_notified = models.DateTimeField(
        blank=True,
        null=True,
        validators=[datetime_not_future],
        verbose_name="Date and time regulatory authorities notified",
    )

    class Meta:
        abstract = True
