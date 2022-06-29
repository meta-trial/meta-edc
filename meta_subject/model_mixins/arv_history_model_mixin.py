from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_model.models import OtherCharField
from edc_reportable import CELLS_PER_MILLIMETER_CUBED_DISPLAY, COPIES_PER_MILLILITER

from meta_lists.models import ArvRegimens, OiProphylaxis


class ArvHistoryModelMixin(models.Model):
    hiv_diagnosis_date = models.DateField(
        verbose_name="When was the diagnosis of HIV made?", null=True, blank=True
    )

    arv_initiation_date = models.DateField(
        verbose_name="Date of start of antiretroviral therapy (ART)",
        null=True,
        blank=True,
    )

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
        verbose_name=("Which antiretroviral therapy regimen is the patient currently on?"),
        null=True,
        blank=False,
    )

    other_current_arv_regimen = OtherCharField(null=True, blank=True)

    current_arv_regimen_start_date = models.DateField(
        verbose_name=(
            "When did the patient start this current antiretroviral therapy regimen?"
        ),
        null=True,
        blank=True,
    )

    has_previous_arv_regimen = models.CharField(
        verbose_name="Has the patient been on any previous regimen?",
        max_length=15,
        choices=YES_NO,
    )

    previous_arv_regimen = models.ForeignKey(
        ArvRegimens,
        on_delete=models.PROTECT,
        related_name="previous_arv_regimen",
        verbose_name=("Which antiretroviral therapy regimen was the patient previously on?"),
        null=True,
        blank=True,
    )

    other_previous_arv_regimen = OtherCharField(null=True, blank=True)

    on_oi_prophylaxis = models.CharField(
        verbose_name=("Is the patient on any prophylaxis against opportunistic infections?"),
        max_length=15,
        choices=YES_NO,
    )

    oi_prophylaxis = models.ManyToManyField(
        OiProphylaxis,
        verbose_name="If YES, which prophylaxis is the patient on?",
        blank=True,
    )

    other_oi_prophylaxis = OtherCharField(null=True, blank=True)

    class Meta:
        abstract = True
