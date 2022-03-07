from django import forms
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_constants.constants import NO
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixin import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from meta_ae.constants import HOSPITAL_CLINIC

from ..models import Delivery


class DeliveryFormValidator(FormValidator):
    def clean(self):
        self.validate_informant()
        self.validate_delivery_location()

    def validate_informant(self):
        self.required_if(
            NO, field="informant_is_patient", field_required="informant_contact"
        )
        self.required_if(
            NO, field="informant_is_patient", field_required="informant_relation"
        )

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


class DeliveryForm(
    SiteModelFormMixin, FormValidatorMixin, ActionItemFormMixin, forms.ModelForm
):

    form_validator_cls = DeliveryFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = Delivery
        fields = "__all__"
