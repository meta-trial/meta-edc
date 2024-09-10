from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixins import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_offstudy.modelform_mixins import OffstudyNonCrfModelFormMixin
from edc_prn.modelform_mixins import PrnFormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from .models import Rx, Substitutions


class SubstitutionsFormValidator(PrnFormValidatorMixin, FormValidator):
    pass


class SubstitutionsForm(
    SiteModelFormMixin,
    OffstudyNonCrfModelFormMixin,
    BaseModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = SubstitutionsFormValidator

    def clean(self):
        if self.cleaned_data.get("sid"):
            try:
                obj = Rx.objects.get(rando_sid=self.cleaned_data.get("sid"))
            except ObjectDoesNotExist:
                raise forms.ValidationError({"sid": "Unknown SID for this trial"})
            else:
                if obj.site.id != self.site.id:
                    raise forms.ValidationError(
                        {
                            "sid": (
                                "Unknown SID for this trial site. "
                                f"Expected SITE {obj.site.id}."
                            )
                        }
                    )
        if self.cleaned_data.get("dispensed_sid"):
            try:
                Rx.objects.get(
                    rando_sid=self.cleaned_data.get("dispensed_sid"),
                )
            except ObjectDoesNotExist:
                raise forms.ValidationError({"dispensed_sid": "Unknown SID for this trial"})

    class Meta:
        model = Substitutions
        fields = "__all__"


class RxForm(forms.ModelForm):

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = Rx
        fields = "__all__"
