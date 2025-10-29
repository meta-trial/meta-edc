from clinicedc_constants import NOT_APPLICABLE
from django import forms
from edc_consent.modelform_mixins import ReviewFieldsModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from edc_utils.date import to_local

from ..consents import consent_v1_ext
from ..models import SubjectConsentV1Ext


class SubjectConsentV1ExtForm(
    SiteModelFormMixin, ReviewFieldsModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    def clean(self):
        cleaned_data = super().clean()
        start_datetime = to_local(consent_v1_ext.start)
        if (
            cleaned_data.get("report_datetime")
            and cleaned_data.get("report_datetime") < start_datetime
        ):
            dt = start_datetime.date().strftime("%Y-%m-%d")
            raise forms.ValidationError(
                {"report_datetime": f"Cannot be before consent approval date {dt}."}
            )

        if cleaned_data.get("agrees_to_extension") == NOT_APPLICABLE:
            raise forms.ValidationError({"agrees_to_extension": "Invalid option"})
        return cleaned_data

    widgets = {  # noqa: RUF012
        "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
    }

    class Meta:
        model = SubjectConsentV1Ext
        fields = "__all__"
        labels = {  # noqa: RUF012
            "study_questions": (
                "I have answered all questions the participant had about the "
                "follow-up extension"
            ),
            "assessment_score": (
                "I have asked the participant questions about the follow-up extension and "
                "the participant has demonstrated understanding"
            ),
        }
