from clinicedc_constants import NO, NOT_EVALUATED, YES
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Index
from edc_constants.choices import YES_NO_NOT_EVALUATED
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.managers import CurrentSiteManager
from edc_sites.model_mixins import SiteModelMixin

from meta_pharmacy.constants import MISSING_SUBJECT_IDENTIFIER
from meta_rando.models import RandomizationList

from .rx import Rx


class MyManager(models.Manager):
    use_in_migrations = True


class Substitutions(NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):
    """A model to capture a CSV file that lists IMP substitutions
    made where a bottle of `sid` is substituted with a bottle of
    `dispensed_sid`.

    The IMP substitutions were not done by any approved procedure. SID
    values are sequential and not designed for human transcription.
    """

    report_datetime = models.DateTimeField(null=True, blank=False)

    row_index = models.IntegerField(null=True)

    rx = models.ForeignKey(Rx, on_delete=models.PROTECT, null=True, blank=True)

    sid = models.IntegerField(verbose_name="SID")

    visit_no = models.IntegerField("Visit Number", null=True, blank=True)

    dispensed_sid = models.IntegerField(verbose_name="Dispensed SID")

    updated_visit_no = models.IntegerField("Visit Number", null=True, blank=True)

    updated_subject_identifier = models.CharField(
        max_length=50, verbose_name="Taken from subject", default="", blank=True
    )

    arm_match = models.CharField(
        max_length=15, choices=YES_NO_NOT_EVALUATED, default=NOT_EVALUATED
    )

    notes = models.TextField(verbose_name="Notes")

    objects = MyManager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords(inherit=True)

    def __str__(self):
        if self.rx:
            return self.rx.subject_identifier
        return str(self.sid)

    def save(self, *args, **kwargs):
        if not self.rx:
            try:
                self.rx = Rx.objects.get(rando_sid=self.sid)
            except ObjectDoesNotExist:
                self.status = MISSING_SUBJECT_IDENTIFIER
            else:
                self.subject_identifier = self.rx.subject_identifier
        else:
            self.subject_identifier = self.rx.subject_identifier
        rando_a = RandomizationList.objects.get(sid=self.sid)
        rando_b = RandomizationList.objects.get(sid=self.dispensed_sid)
        if rando_a.assignment != rando_b.assignment:
            self.arm_match = NO
        else:
            self.arm_match = YES

        super().save(*args, **kwargs)

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name_plural = "IMP Substitutions"
        verbose_name = "IMP Substitution"
        indexes = (
            Index(fields=["sid", "dispensed_sid", "subject_identifier"]),
            Index(fields=["row_index"]),
        )
