from django import forms
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from edc_dashboard.url_names import url_names
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin

from ..form_validators import SubjectRefusalFormValidator
from ..models import SubjectRefusal, SubjectScreening


class ScreeningFormMixin:
    def clean(self):
        cleaned_data = super().clean()
        screening_identifier = cleaned_data.get("screening_identifier")
        if screening_identifier:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=screening_identifier
            )
            if not subject_screening.eligible:
                url_name = url_names.get("screening_listboard_url")
                url = reverse(
                    url_name,
                    kwargs={"screening_identifier": self.instance.screening_identifier},
                )
                msg = mark_safe(
                    "Not allowed. Subject is not eligible. "
                    f'See subject <A href="{url}?q={screening_identifier}">'
                    f"{screening_identifier}</A>"
                )
                raise forms.ValidationError(msg)
        return cleaned_data


class SubjectRefusalForm(
    AlreadyConsentedFormMixin, ScreeningFormMixin, FormValidatorMixin, forms.ModelForm
):

    form_validator_cls = SubjectRefusalFormValidator

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = SubjectRefusal
        fields = "__all__"
