from clinicedc_constants import COMPLETE, DONE, NOT_APPLICABLE, NOT_AVAILABLE, YES
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_glucose.model_mixin_factories import (
    fasting_model_mixin_factory,
    ogtt_model_mixin_factory,
)
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_qareports.model_mixins import NoteModelMixin

NOTE_STATUSES = (
    (COMPLETE, "Complete"),
    (NOT_AVAILABLE, "Not available"),
)


class MissingOgttNote(
    fasting_model_mixin_factory(
        None,
        fasting=models.CharField(
            verbose_name="Did the participant fast?",
            max_length=15,
            choices=YES_NO_NA,
            default=NOT_APPLICABLE,
            blank=False,
        ),
    ),
    ogtt_model_mixin_factory("ogtt"),
    UniqueSubjectIdentifierFieldMixin,
    NoteModelMixin,
):
    """Model class to replace default `Note` model used with
    QA Report 'Screening: Missing OGTT'.
    """

    result_status = models.CharField(
        verbose_name="Is the OGTT result available", max_length=25, default=YES, choices=YES_NO
    )

    status = models.CharField(max_length=25, default=DONE, choices=NOTE_STATUSES)

    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self._meta.verbose_name}: {self.subject_identifier}"

    def save(self, *args, **kwargs):
        if self.result_status == YES:
            self.status = COMPLETE
        else:
            self.status = NOT_AVAILABLE
        super().save(*args, **kwargs)

    class Meta(UniqueSubjectIdentifierFieldMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Screening: Missing OGTT Note"
        verbose_name_plural = "Screening: Missing OGTT Notes"
