from clinicedc_constants import NOT_APPLICABLE, NULL_STRING
from clinicedc_constants.choices import YES_NO_NA
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _


class SpfqRefusalModelMixin(models.Model):
    contact_attempted = models.CharField(
        verbose_name=_("Were any attempts made to contact the participant?"),
        max_length=25,
        choices=YES_NO_NA,
    )

    contact_attempts_count = models.IntegerField(
        verbose_name=_("Number of attempts made to contact participant"),
        validators=[MinValueValidator(1)],
        help_text=_("Multiple attempts on the same day count as a single attempt."),
        null=True,
        blank=True,
    )

    contact_made = models.CharField(
        verbose_name=_("Was contact made with the participant?"),
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    contact_attempts_explained = models.TextField(
        verbose_name=_("If contact not made and less than 3 attempts, please explain"),
        default=NULL_STRING,
        blank=True,
    )

    reason = models.TextField(
        verbose_name="Why is this participant not consenting to the sub-study?",
        default=NULL_STRING,
    )

    class Meta:
        abstract = True
