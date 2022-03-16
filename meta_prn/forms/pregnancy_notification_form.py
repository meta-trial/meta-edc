from django import forms
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_constants.constants import NO, YES
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixin import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from meta_subject.models import UrinePregnancy

from ..models import PregnancyNotification


class PregnancyNotificationFormValidator(FormValidator):
    def clean(self):
        self.required_if(
            NO, field="bhcg_confirmed", field_required="unconfirmed_details"
        )
        if self.instance.id is None and self.cleaned_data.get("bhcg_confirmed") == YES:
            if not UrinePregnancy.objects.filter(
                subject_visit__subject_identifier=self.cleaned_data.get(
                    "subject_identifier"
                ),
                notified=False,
                assay_date__lte=self.cleaned_data.get("report_datetime"),
            ).exists():
                raise forms.ValidationError(
                    f"Invalid. A positive Urine βhCG cannot be found. See {UrinePregnancy._meta.verbose_name}"
                )


class PregnancyNotificationForm(
    SiteModelFormMixin, FormValidatorMixin, ActionItemFormMixin, forms.ModelForm
):

    form_validator_cls = PregnancyNotificationFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = PregnancyNotification
        fields = "__all__"
