from django import forms
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import HepatitisTest


class HepatitisTestFormValidator(FormValidator):
    def clean(self):

        self.required_if(YES, field="hbsag_performed", field_required="hbsag")
        self.required_if(YES, field="hbsag_performed", field_required="hbsag_date")
        self.required_if(YES, field="hcv_performed", field_required="hcv")
        self.required_if(YES, field="hcv_performed", field_required="hcv_date")


class HepatitisTestForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = HepatitisTestFormValidator

    class Meta:
        model = HepatitisTest
        fields = "__all__"
