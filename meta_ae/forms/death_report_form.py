from django import forms
from edc_adverse_event.form_validator_mixins import DeathReportFormValidatorMixin
from edc_adverse_event.modelform_mixins import DeathReportModelFormMixin
from edc_constants.constants import OTHER
from edc_form_validators import FormValidator

from ..constants import HOSPITAL_CLINIC
from ..models import DeathReport


class DeathReportFormValidator(DeathReportFormValidatorMixin, FormValidator):
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

    form_validator_cls = DeathReportFormValidator

    class Meta(DeathReportModelFormMixin.Meta):
        model = DeathReport
        fields = "__all__"
