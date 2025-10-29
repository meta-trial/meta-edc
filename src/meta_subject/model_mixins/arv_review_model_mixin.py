from clinicedc_constants import COPIES_PER_MILLILITER, NULL_STRING
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_model.models import OtherCharField
from edc_reportable.units import CELLS_PER_MILLIMETER_CUBED_DISPLAY

from meta_lists.models import ArvRegimens


class ArvReviewModelMixin(models.Model):
    viral_load = models.IntegerField(
        verbose_name="Last viral load",
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        null=True,
        blank=True,
        help_text=COPIES_PER_MILLILITER,
    )

    viral_load_date = models.DateField(
        verbose_name="Date of last viral load", null=True, blank=True
    )

    cd4 = models.IntegerField(
        verbose_name="Last CD4",
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        null=True,
        blank=True,
        help_text=CELLS_PER_MILLIMETER_CUBED_DISPLAY,
    )

    cd4_date = models.DateField(verbose_name="Date of last CD4", null=True, blank=True)

    current_arv_regimen = models.ForeignKey(
        ArvRegimens,
        on_delete=models.PROTECT,
        related_name="current_arv_regimen",
        verbose_name="Which antiretroviral therapy regimen is the patient currently on?",
        null=True,
        blank=False,
    )

    other_current_arv_regimen = OtherCharField(default=NULL_STRING, blank=True)

    current_arv_regimen_start_date = models.DateField(
        verbose_name=(
            "When did the patient start this current antiretroviral therapy regimen?"
        ),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
