from django.db import models
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_offstudy.model_mixins import OffstudyNonCrfModelMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_sites.models import SiteModelMixin
from edc_visit_tracking.managers import VisitCurrentSiteManager, VisitModelManager
from edc_visit_tracking.model_mixins import VisitModelMixin

from ..choices import INFO_SOURCE, VISIT_REASON, VISIT_UNSCHEDULED_REASON


class SubjectVisit(
    VisitModelMixin,
    ReferenceModelMixin,
    CreatesMetadataModelMixin,
    SiteModelMixin,
    RequiresConsentFieldsModelMixin,
    OffstudyNonCrfModelMixin,
    BaseUuidModel,
):

    """A model completed by the user that captures the covering
    information for the data collected for this timepoint/appointment,
    e.g.report_datetime.
    """

    # override default
    reason = models.CharField(
        verbose_name="What is the reason for this visit report?",
        max_length=25,
        choices=VISIT_REASON,
        help_text="If 'missed', fill in the separate missed visit report",
    )

    # override default
    reason_unscheduled = models.CharField(
        verbose_name="If 'unscheduled', provide reason for the unscheduled visit",
        max_length=25,
        choices=VISIT_UNSCHEDULED_REASON,
        default=NOT_APPLICABLE,
    )

    unschedule_self_referral = models.CharField(
        verbose_name="If 'unschedule', is this a self-referral?",
        max_length=25,
        choices=YES_NO,
        default=NO,
    )

    unschedule_detail = models.TextField(
        verbose_name="If 'unschedule', please provide further details, if any",
        null=True,
        blank=True,
    )

    # override default
    info_source = models.CharField(
        verbose_name="What is the main source of this information?",
        max_length=25,
        choices=INFO_SOURCE,
    )

    on_site = VisitCurrentSiteManager()

    objects = VisitModelManager()

    history = HistoricalRecords()

    class Meta(VisitModelMixin.Meta, BaseUuidModel.Meta):
        pass
