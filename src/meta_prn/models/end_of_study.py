from clinicedc_constants import (
    DEAD,
    DELIVERY,
    DIABETES,
    LTFU,
    NOT_APPLICABLE,
    NULL_STRING,
    OTHER,
    PREGNANCY,
    TOXICITY,
)
from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO_NA
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_offstudy.constants import (
    COMPLETED_FOLLOWUP,
    END_OF_STUDY_ACTION,
    LATE_EXCLUSION,
    WITHDRAWAL,
)
from edc_offstudy.model_mixins import OffstudyModelMixin
from edc_sites.model_mixins import SiteModelMixin
from edc_transfer.constants import TRANSFERRED

from meta_lists.models import OffstudyReasons

from ..choices import CLINICAL_WITHDRAWAL_REASONS, TOXICITY_WITHDRAWAL_REASONS
from ..constants import CLINICAL_WITHDRAWAL, COMPLETED_FOLLOWUP_48

# TODO: confirm all appointments are either new, incomplete or done
# TODO: take off study meds but coninue followup (WITHDRAWAL)
# TODO: follow on new schedule, if permanently off drug (Single 36m visit)

# TODO: add label for "End of followup as per protocol FEB2026"


class EndOfStudy(ActionModelMixin, SiteModelMixin, OffstudyModelMixin, BaseUuidModel):
    action_name = END_OF_STUDY_ACTION

    last_seen_date = models.DateField(
        verbose_name="Date patient was last seen",
        validators=[date_not_future],
        blank=False,
        null=True,
    )

    offstudy_reason = models.ForeignKey(
        OffstudyReasons,
        verbose_name="Reason patient was terminated from the study",
        on_delete=models.PROTECT,
        null=True,
        limit_choices_to={
            "name__in": [
                COMPLETED_FOLLOWUP,
                COMPLETED_FOLLOWUP_48,
                DIABETES,
                DELIVERY,
                PREGNANCY,
                CLINICAL_WITHDRAWAL,
                DEAD,
                LTFU,
                TOXICITY,
                TRANSFERRED,
                WITHDRAWAL,
                LATE_EXCLUSION,
                OTHER,
            ]
        },
    )

    other_offstudy_reason = models.TextField(
        verbose_name="If OTHER, please specify",
        max_length=500,
        blank=True,
        default=NULL_STRING,
    )

    # TODO: 6m off drug and duration ?? See SOP
    ltfu_date = models.DateField(
        verbose_name="Date lost to followup, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
        help_text="A Loss to followup report must be on file",
    )

    death_date = models.DateField(
        verbose_name="Date of death, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
        help_text="A Death report must be on file",
    )

    pregnancy_date = models.DateField(
        verbose_name="Date pregnancy known/UPT, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
        help_text=(
            "A UPT CRF must be on file and participant not on the "
            "delivery schedule. Use UPT date or, if UPT not needed, "
            "use report date on last UPT CRF."
        ),
    )

    delivery_date = models.DateField(
        verbose_name="Date of delivery, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
        help_text=(
            "A Delivery CRF must be on file. Use delivery date, "
            "if reported, or report date from Delivery CRF"
        ),
    )

    clinical_withdrawal_reason = models.CharField(
        verbose_name=(
            "If the patient was withdrawn on CLINICAL grounds, please specify PRIMARY reason"
        ),
        max_length=25,
        choices=CLINICAL_WITHDRAWAL_REASONS,
        default=NOT_APPLICABLE,
    )

    clinical_withdrawal_reason_other = models.TextField(
        verbose_name="If withdrawn for 'other' condition, please explain",
        max_length=500,
        blank=True,
        default=NULL_STRING,
    )

    clinical_withdrawal_investigator_decision = models.TextField(
        verbose_name="If withdrawl was an 'investigator decision', please explain ...",
        max_length=500,
        blank=True,
        default=NULL_STRING,
    )

    toxicity_withdrawal_reason = models.CharField(
        verbose_name=" If the patient experienced an unacceptable toxicity', please explain",
        max_length=25,
        choices=TOXICITY_WITHDRAWAL_REASONS,
        default=NOT_APPLICABLE,
    )

    toxicity_withdrawal_reason_other = models.TextField(
        verbose_name="If 'other toxicity', please specify ...",
        max_length=500,
        blank=True,
        default=NULL_STRING,
    )

    transfer_date = models.DateField(
        verbose_name="Date of transfer, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
        help_text="A Transfer form must be on file.",
    )

    transferred_consent = models.CharField(
        verbose_name="If transferred, has the patient provided consent to be followed-up?",
        choices=YES_NO_NA,
        max_length=15,
        default=NOT_APPLICABLE,
    )

    comment = models.TextField(
        verbose_name="Please provide further details if possible",
        max_length=500,
        blank=True,
        default=NULL_STRING,
    )

    class Meta(OffstudyModelMixin.Meta):
        verbose_name = "End of Study"
        verbose_name_plural = "End of Study"
