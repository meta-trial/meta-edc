from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_constants.constants import NO, OTHER
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import INVALID_ERROR
from edc_utils import formatted_date

from meta_ae.constants import HOSPITAL_CLINIC
from meta_prn.models import PregnancyNotification

from ..models import Delivery


class DeliveryFormValidator(CrfFormValidator):
    def clean(self):
        try:
            pregnancy_notification = PregnancyNotification.objects.get(
                subject_identifier=self.cleaned_data.get("subject_visit").subject_identifier
            )
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                f"{PregnancyNotification._meta.verbose_name} not found."
            )

        self.required_if(
            NO, field="info_available", field_required="info_not_available_reason"
        )

        self.validate_informant()

        self.validate_delivery_date_with_upt(pregnancy_notification)

        self.validate_delivery_location()

    def validate_informant(self):
        self.required_if(OTHER, field="info_source", field_required="info_source_other")
        self.required_if(NO, field="info_source", field_required="informant_relation")
        self.validate_other_specify(
            field="informant_relation", other_specify_field="informant_relation_other"
        )

    def validate_delivery_date_with_upt(self, pregnancy_notification):
        """Delivery date must be after the UPT date"""
        if (
            self.cleaned_data.get("delivery_datetime")
            and self.cleaned_data.get("report_datetime")
            and self.cleaned_data.get("report_datetime").date()
            < self.cleaned_data.get("delivery_datetime").date()
        ):
            self.raise_validation_error(
                {"delivery_datetime": "Expected a date on or before the report date above"},
                INVALID_ERROR,
            )
        if (
            self.cleaned_data.get("delivery_datetime")
            and (
                pregnancy_notification.bhcg_date
                or pregnancy_notification.report_datetime.date()
            )
            > self.cleaned_data.get("delivery_datetime").date()
        ):
            dte = formatted_date(
                pregnancy_notification.bhcg_date
                or pregnancy_notification.report_datetime.date()
            )
            word = "UPT date" if pregnancy_notification.bhcg_date else "Pregnancy report date"
            self.raise_validation_error(
                {
                    "delivery_datetime": (
                        f"Expected a date after the {word} on the "
                        f"{pregnancy_notification._meta.verbose_name}. {word} was {dte}."
                    )
                },
                INVALID_ERROR,
            )

    def validate_delivery_location(self):
        self.required_if(
            HOSPITAL_CLINIC,
            field="delivery_location",
            field_required="delivery_location_name",
        )
        self.validate_other_specify(
            field="delivery_location", other_specify_field="delivery_location_other"
        )


class DeliveryForm(CrfModelFormMixin, ActionItemCrfFormMixin, forms.ModelForm):

    form_validator_cls = DeliveryFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = Delivery
        fields = "__all__"
