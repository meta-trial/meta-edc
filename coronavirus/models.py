from django.conf import settings
from django.db import models
from django.db.models import PROTECT
from edc_crf.model_mixins import CrfModelMixin
from edc_model import models as edc_models
from edc_model.validators import datetime_not_future
from edc_protocol.validators import datetime_not_before_study_start
from edc_sites.models import SiteModelMixin
from edc_utils import get_utcnow
from sarscov2.model_mixins import CoronaKapModelMixin, CoronaKapDiseaseModelMixin


class CoronaKap(
    CoronaKapDiseaseModelMixin,
    CoronaKapModelMixin,
    SiteModelMixin,
    edc_models.BaseUuidModel,
):

    subject_identifier = models.CharField(
        max_length=50, unique=True, verbose_name="Subject identifier", null=True,
    )

    screening_identifier = models.CharField(
        max_length=50, unique=True, verbose_name="Screening identifier", null=True,
    )

    subject_visit = models.ForeignKey(
        settings.SUBJECT_VISIT_MODEL, on_delete=PROTECT, null=True
    )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[datetime_not_before_study_start, datetime_not_future],
        default=get_utcnow,
        help_text=(
            "If reporting today, use today's date/time, otherwise use "
            "the date/time this information was reported."
        ),
    )

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Coronavirus Knowledge, Attitudes, and Practices"
        verbose_name_plural = "Coronavirus Knowledge, Attitudes, and Practices"
