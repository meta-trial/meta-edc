from django.contrib.sites.models import Site
from django.db import models
from django.db.models import PROTECT


class UnattendedThreeInRow2(models.Model):

    subject_identifier = models.CharField(max_length=25)

    site = models.ForeignKey(Site, on_delete=PROTECT)

    first = models.CharField(max_length=25)

    second = models.CharField(max_length=25)

    third = models.CharField(max_length=25)

    interval_days = models.IntegerField()

    from_now_days = models.IntegerField()

    missed_count = models.IntegerField()

    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "unattended_three_in_row2_view"
        verbose_name = "R110: Unattended appointments: Three in a row (with missed)"
        verbose_name_plural = "R110: Unattended appointments: Three in a row (with missed)"
