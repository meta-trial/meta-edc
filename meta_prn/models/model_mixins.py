from django.db import models
from edc_model.validators import date_not_future, datetime_not_future
from edc_protocol.validators import (
    date_not_before_study_start,
    datetime_not_before_study_start,
)


class OffStudyModelMixin(models.Model):

    offstudy_datetime = models.DateTimeField(
        verbose_name="Date patient was terminated from the study",
        validators=[datetime_not_future],
        blank=False,
        null=True,
    )

    def save(self, *args, **kwargs):
        try:
            self.offstudy_datetime.date()
        except AttributeError:
            dt = self.offstudy_datetime.date()
            date_not_before_study_start(dt)
            date_not_future(dt)
        else:
            datetime_not_before_study_start(self.offstudy_datetime)
            datetime_not_future(self.offstudy_datetime)
        self.report_datetime = self.offstudy_datetime
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
