from django import forms
from edc_constants.constants import YES
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import PregnancyUpdate


class PregnancyUpdateFormValidator(CrfFormValidator):
    def clean(self):
        self.required_if(YES, field="contact", field_required="comment")


class PregnancyUpdateForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = PregnancyUpdateFormValidator

    class Meta:
        model = PregnancyUpdate
        fields = "__all__"
