from dateutil.relativedelta import relativedelta
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_constants.constants import FEMALE, NO, YES
from edc_form_validators import INVALID_ERROR
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixin import FormValidatorMixin
from edc_registration.models import RegisteredSubject
from edc_sites.forms import SiteModelFormMixin
from edc_visit_schedule.constants import DAY1

from meta_subject.models import UrinePregnancy

from ..models import PregnancyNotification


class PregnancyNotificationFormValidator(FormValidator):
    def clean(self):
        try:
            RegisteredSubject.objects.get(
                subject_identifier=self.cleaned_data.get("subject_identifier"), gender=FEMALE
            )
        except ObjectDoesNotExist:
            self.raise_validation_error("Participant is not female.")

        self.required_if(NO, field="bhcg_confirmed", field_required="unconfirmed_details")
        self.required_if(YES, field="bhcg_confirmed", field_required="bhcg_date")
        self.validate_bhcg()
        self.validate_edd()

    def validate_bhcg(self):
        if (
            self.cleaned_data.get("bhcg_date")
            and self.cleaned_data.get("report_datetime")
            and self.cleaned_data.get("bhcg_date")
            > self.cleaned_data.get("report_datetime").date()
        ):
            self.raise_validation_error(
                {"bhcg_date": "Expected a date on or before the report date/time."},
                INVALID_ERROR,
            )
        if (
            self.instance.id is None
            and self.cleaned_data.get("bhcg_confirmed") == YES
            and self.cleaned_data.get("bhcg_date")
        ):
            if (
                not UrinePregnancy.objects.filter(
                    subject_visit__subject_identifier=self.cleaned_data.get(
                        "subject_identifier"
                    ),
                    notified=False,
                    assay_date=self.cleaned_data.get("bhcg_date"),
                )
                .exclude(subject_visit__visit_code=DAY1, subject_visit__visit_code_sequence=0)
                .exists()
            ):
                self.raise_validation_error(
                    "Invalid. A positive Urine βhCG cannot be found. "
                    "Ensure the UPT has been entered, the date matches, and the "
                    "UPT is not a baseline UPT. "
                    f"See also PRN CRF {UrinePregnancy._meta.verbose_name}",
                    INVALID_ERROR,
                )

    def validate_edd(self):
        if (
            self.cleaned_data.get("edd")
            and self.cleaned_data.get("bhcg_date")
            and self.cleaned_data.get("edd") < self.cleaned_data.get("bhcg_date")
        ):
            self.raise_validation_error(
                {"edd": "Expected a date after the UPT date."}, INVALID_ERROR
            )
        if (
            self.cleaned_data.get("edd")
            and self.cleaned_data.get("bhcg_date")
            and self.cleaned_data.get("edd")
            > self.cleaned_data.get("bhcg_date") + relativedelta(months=9)
        ):
            self.raise_validation_error(
                {"edd": "Expected a date within 9 months of UPT date."}, INVALID_ERROR
            )
        if (
            self.cleaned_data.get("report_datetime")
            and not self.cleaned_data.get("bhcg_date")
            and self.cleaned_data.get("bhcg_confirmed") == NO
        ):
            if (
                self.cleaned_data.get("report_datetime")
                and self.cleaned_data.get("edd")
                < self.cleaned_data.get("report_datetime").date()
            ):
                self.raise_validation_error(
                    {"edd": "Expected a date after the report date."}, INVALID_ERROR
                )
            if self.cleaned_data.get("report_datetime") and self.cleaned_data.get(
                "edd"
            ) > self.cleaned_data.get("report_datetime").date() + relativedelta(months=9):
                self.raise_validation_error(
                    {"edd": "Expected a date within 9 months of report date."}, INVALID_ERROR
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
