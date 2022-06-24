from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from edc_constants.choices import GENDER, YES_NO, YES_NO_NA
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils.date import get_utcnow

from ..choices import ETHNICITY
from .subject_screening import SubjectScreening


class IcpReferralError(Exception):
    pass


class IcpReferralManager(models.Manager):
    def get_by_natural_key(self, screening_identifier):
        return self.get(screening_identifier=screening_identifier)


class IcpReferral(SiteModelMixin, BaseUuidModel):
    """ "Not used"""

    subject_screening = models.OneToOneField(
        SubjectScreening, null=True, on_delete=models.PROTECT
    )

    screening_identifier = models.CharField(
        verbose_name="META Screening Identifier", max_length=25, unique=True
    )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=get_utcnow,
        help_text="Date and time of report.",
    )

    hospital_identifier = models.CharField(max_length=25, unique=True)

    gender = models.CharField(choices=GENDER, max_length=10)

    age_in_years = models.IntegerField()

    initials = models.CharField(max_length=3)

    ethnicity = models.CharField(
        max_length=15, choices=ETHNICITY, help_text="Used for eGFR calculation"
    )

    hiv_pos = models.CharField(verbose_name="HIV positive", max_length=15, choices=YES_NO)

    art_six_months = models.CharField(
        verbose_name="On anti-retroviral therapy for at least 6 months",
        max_length=15,
        choices=YES_NO_NA,
    )

    fbg_value = models.DecimalField(
        verbose_name="FBG level",
        max_digits=8,
        decimal_places=4,
        null=True,
        help_text="mmol/L",
    )

    hba1c_value = models.DecimalField(
        verbose_name="HbA1c",
        max_digits=8,
        decimal_places=4,
        null=True,
        help_text="in %",
    )

    ogtt_value = models.DecimalField(
        verbose_name="Blood glucose levels 2-hours after glucose solution given",
        max_digits=8,
        decimal_places=4,
        null=True,
        help_text="mmol/L",
    )

    meta_eligible = models.BooleanField(verbose_name="META eligibile")

    meta_eligibility_datetime = models.DateTimeField(
        null=True, help_text="Date and time META eligibility was determined"
    )

    referred = models.BooleanField(verbose_name="Referred", default=False)

    referred = models.DateTimeField(null=True, help_text="Date and time of referral")

    referral_reasons = models.TextField(null=True)

    on_site = CurrentSiteManager()

    objects = IcpReferralManager()

    history = HistoricalRecords(inherit=True)

    def save(self, *args, **kwargs):
        try:
            SubjectScreening.objects.get(screening_identifier=self.screening_identifier)
        except ObjectDoesNotExist:
            raise IcpReferralError(
                f"Invalid META screening identifier. Got {self.screening_identifier}"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.screening_identifier} {self.gender} {self.age_in_years}"

    def natural_key(self):
        return (self.screening_identifier,)  # noqa

    class Meta:
        pass
