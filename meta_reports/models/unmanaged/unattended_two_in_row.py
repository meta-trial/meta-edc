from django.contrib.sites.models import Site
from django.db import models
from django.db.models import PROTECT


class UnattendedTwoInRow(models.Model):

    subject_identifier = models.CharField(max_length=25)

    site = models.ForeignKey(Site, on_delete=PROTECT)

    appt_datetime = models.DateTimeField()

    first = models.CharField(max_length=25)

    second = models.CharField(max_length=25)

    interval_days = models.IntegerField()

    from_now_days = models.IntegerField()

    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "unattended_two_in_row_view"
        verbose_name = "R120: Unattended appointments: Two in a row"
        verbose_name_plural = "R120: Unattended appointments: Two in a row"
