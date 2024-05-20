from edc_form_validators import FormValidator


class DmDiagnosisFormValidator(FormValidator):
    def clean(self):
        self.required_if_true(self.cleaned_data.get("report_date"), field_required="utestid")
        self.required_if_true(self.cleaned_data.get("utestid"), field_required="value")
