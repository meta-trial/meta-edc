from edc_model import models as edc_models

from ..model_mixins import AeReviewModelMixin


class AeLocalReview(AeReviewModelMixin, edc_models.BaseUuidModel):
    """Not used"""

    class Meta:
        verbose_name = "AE Local Review"
