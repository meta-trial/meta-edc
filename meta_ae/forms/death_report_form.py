from django import forms
from django.apps import apps as django_apps
from edc_adverse_event.forms import DeathReportModelFormMixin
from edc_constants.constants import OTHER
from edc_form_validators import FormValidator

from ..constants import HOSPITAL_CLINIC
from ..models import DeathReport


class DeathReportFormValidator(FormValidator):
    @property
    def cause_of_death_model_cls(self):
        return django_apps.get_model("edc_adverse_event.causeofdeath")

    def clean(self):

        self.required_if(
            HOSPITAL_CLINIC,
            field="death_location",
            field_required="hospital_name",
        )

        self.validate_other_specify(
            field="informant_relationship",
            other_specify_field="other_informant_relationship",
        )

        other = self.cause_of_death_model_cls.objects.get(name=OTHER)
        self.validate_other_specify(
            field="cause_of_death",
            other_specify_field="cause_of_death_other",
            other_stored_value=other.name,
        )

        self.validate_other_specify(
            field="secondary_cause_of_death",
            other_specify_field="secondary_cause_of_death_other",
            other_stored_value=other.name,
        )


class DeathReportForm(DeathReportModelFormMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label="Subject identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = DeathReport
        fields = "__all__"
