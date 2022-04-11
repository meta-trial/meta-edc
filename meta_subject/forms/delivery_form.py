from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_action_item.forms import ActionItemFormMixin
from edc_constants.constants import NO, OTHER
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from meta_ae.constants import HOSPITAL_CLINIC
from meta_prn.models import PregnancyNotification

from ..models import Delivery


class DeliveryFormValidator(FormValidator):
    def clean(self):
        try:
            PregnancyNotification.objects.get(
                subject_identifier=self.cleaned_data.get(
                    "subject_visit"
                ).subject_identifier
            )
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                f"{PregnancyNotification._meta.verbose_name} not found."
            )

        self.required_if(
            NO, field="info_available", field_required="info_not_available_reason"
        )
        self.required_if(
            YES, field="info_available", field_required="info_not_available_reason"
        )

        self.validate_informant()

        self.validate_delivery_location()

    def validate_informant(self):
        self.required_if(OTHER, field="info_source", field_required="info_source_other")
        self.required_if(NO, field="info_source", field_required="informant_relation")

        self.validate_other_specify(
            field="informant_relation", field_required="informant_relation_other"
        )

    def validate_delivery_location(self):
        self.validate_other_specify(
            field="delivery_location", field_required="delivery_location_other"
        )
        self.required_if(
            HOSPITAL_CLINIC,
            field="delivery_location",
            field_required="delivery_location_name",
        )
        self.validate_other_specify(
            field="delivery_location", field_required="delivery_location_other"
        )


class DeliveryForm(CrfModelFormMixin, ActionItemFormMixin, forms.ModelForm):

    form_validator_cls = DeliveryFormValidator

    class Meta:
        model = Delivery
        fields = "__all__"
