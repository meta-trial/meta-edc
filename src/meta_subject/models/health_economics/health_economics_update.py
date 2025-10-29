from clinicedc_constants import NOT_APPLICABLE
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from edc_constants.choices import YES_NO
from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_he.choices import RELATIONSHIP_CHOICES, STATUS
from edc_he.model_mixin_factories import income_model_mixin_factory
from edc_he.model_mixins import HouseholdModelMixin
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField

from ...model_mixins import CrfModelMixin


class HealthEconomicsUpdate(
    HouseholdModelMixin,
    income_model_mixin_factory(
        field_data={
            "avg_income": _(
                "Thinking over the last 12 months, can you tell me "
                "what the average earnings of the household have been?"
            ),
        }
    ),
    SingletonCrfModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    """A user model to learn about the household, wealth and
    opportunities in the community

    Introduced 22 FEB 2024
    """

    hoh = models.CharField(
        verbose_name=_("Are you the household head?"),
        max_length=15,
        choices=YES_NO,
        help_text=_(
            "By head of the household we mean the main decision "
            "maker in the household. The head can be either male or "
            "female. If two people are equal decision-makers, take "
            "the older person."
        ),
    )

    relationship_to_hoh = models.CharField(
        verbose_name=_("If No, what is your relationship to the household head?"),
        max_length=25,
        choices=RELATIONSHIP_CHOICES,
        default=NOT_APPLICABLE,
        help_text=_("Not applicable if patient is head of household"),
    )

    relationship_to_hoh_other = OtherCharField(
        verbose_name=_("If OTHER relationship, specify ..."),
    )

    rooms = models.IntegerField(
        verbose_name=_(
            "How many rooms does your dwelling have in total, without counting "
            "the bathrooms/ toilets or hallways/passageways?"
        ),
        validators=[MinValueValidator(1), MaxValueValidator(30)],
    )

    bedrooms = models.IntegerField(
        verbose_name=_("How many rooms are used for sleeping in your dwelling?"),
        validators=[MinValueValidator(0), MaxValueValidator(30)],
    )

    beds = models.IntegerField(
        verbose_name=_("How many beds does your dwelling have in total?"),
        validators=[MinValueValidator(0), MaxValueValidator(30)],
    )

    external_dependents = models.IntegerField(
        verbose_name=_(
            "Outside of this household, how many other people depend on this "
            "household's income?"
        ),
        validators=[MinValueValidator(0), MaxValueValidator(15)],
        help_text=_(
            "Insert '0' if no dependents other than the members in the household roster"
        ),
    )

    financial_status = models.CharField(
        verbose_name=_("Would you say your household's financial situation is?"),
        max_length=25,
        choices=STATUS,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health Economics: Baseline"
        verbose_name_plural = "Health Economics: Baseline"
