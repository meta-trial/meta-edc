from django import forms
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import PregnancyUpdate


class PregnancyUpdateFormValidator(FormValidator):
    def clean(self):
        self.required_if(YES, field="contact", field_required="comment")


class PregnancyUpdateForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = PregnancyUpdateFormValidator

    class Meta:
        model = PregnancyUpdate
        fields = "__all__"
