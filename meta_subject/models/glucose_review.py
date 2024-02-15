from django.db import models
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class RepeatFbgRequest(CrfModelMixin, BaseUuidModel):
    """A model completed by the user to schedule a repeat FBG
    to determine if participant meets endpoint criteria.
    """

    next_fbg_date = models.DateField("Date particpant will attend to repeat FBG")

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        pass
