from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import OtherArvRegimens


class OtherArvRegimensFormValidator(FormValidator):
    def clean(self):
        pass


class OtherArvRegimensForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = OtherArvRegimensFormValidator

    class Meta:
        model = OtherArvRegimens
        fields = "__all__"
