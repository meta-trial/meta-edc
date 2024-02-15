from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_adverse_event.constants import HOSPITALIZATION_ACTION
from edc_adverse_event.model_mixins import HospitalizationModelMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin


class Hospitalization(
    SiteModelMixin, ActionModelMixin, HospitalizationModelMixin, BaseUuidModel
):
    action_name = HOSPITALIZATION_ACTION

    class Meta(HospitalizationModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Hospitalization"
        verbose_name_plural = "Hospitalization"
        indexes = (
            HospitalizationModelMixin.Meta.indexes
            + BaseUuidModel.Meta.indexes
            + [models.Index(fields=["subject_identifier", "site"])]
        )
