from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixins import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_offstudy.modelform_mixins import OffstudyNonCrfModelFormMixin
from edc_prn.modelform_mixins import PrnFormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from meta_rando.models import RandomizationList

from ..models import Rx, Substitutions


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
            except ObjectDoesNotExist as e:
                raise forms.ValidationError({"sid": "Unknown SID for this trial"}) from e
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
                RandomizationList.objects.get(
                    sid=self.cleaned_data.get("dispensed_sid"),
                )
            except ObjectDoesNotExist as e:
                raise forms.ValidationError(
                    {"dispensed_sid": "Invalid SID for this trial"}
                ) from e

    class Meta:
        model = Substitutions
        fields = "__all__"
