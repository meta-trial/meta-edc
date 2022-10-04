from urllib import parse

from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.html import format_html
from edc_action_item.models import ActionType
from edc_adverse_event.form_validator_mixins import (
    RequiresDeathReportFormValidatorMixin,
)
from edc_consent.constants import CONSENT_WITHDRAWAL
from edc_constants.constants import DEAD, DELIVERY, PREGNANCY, TOXICITY
from edc_form_validators import INVALID_ERROR, FormValidator
from edc_ltfu.constants import LTFU
from edc_ltfu.modelform_mixins import RequiresLtfuFormValidatorMixin
from edc_offstudy.constants import COMPLETED_FOLLOWUP
from edc_offstudy.utils import OffstudyError
from edc_prn.modelform_mixins import PrnFormValidatorMixin
from edc_transfer.constants import TRANSFERRED
from edc_utils import formatted_date
from edc_visit_schedule.constants import MONTH36
from edc_visit_schedule.utils import off_all_schedules_or_raise

from ..constants import (
    CLINICAL_WITHDRAWAL,
    INVESTIGATOR_DECISION,
    OFFSTUDY_MEDICATION_ACTION,
)


class EndOfStudyFormValidator(
    RequiresDeathReportFormValidatorMixin,
    RequiresLtfuFormValidatorMixin,
    PrnFormValidatorMixin,
    FormValidator,
):
    death_report_model = "meta_ae.deathreport"
    ltfu_model = None

    def clean(self):

        self.confirm_off_all_schedules()
        self.validate_study_medication_status()
        self.validate_offstudy_datetime_against_last_seen_date()

        self.validate_completed_36m()

        self.required_if(DEAD, field="offstudy_reason", field_required="death_date")
        self.validate_death_report_if_deceased()

        self.required_if(PREGNANCY, field="offstudy_reason", field_required="pregnancy_date")
        self.validate_pregnancy()

        self.required_if(DELIVERY, field="offstudy_reason", field_required="delivery_date")
        self.validate_delivery()

        self.required_if(TRANSFERRED, field="offstudy_reason", field_required="transfer_date")
        self.validate_transfer()

        self.required_if(LTFU, field="offstudy_reason", field_required="ltfu_date")
        self.validate_ltfu()

        self.applicable_if(
            TOXICITY, field="offstudy_reason", field_applicable="toxicity_withdrawal_reason"
        )
        self.validate_other_specify(
            field="toxicity_withdrawal_reason",
            other_specify_field="toxicity_withdrawal_reason_other",
        )

        self.applicable_if(
            CLINICAL_WITHDRAWAL,
            field="offstudy_reason",
            field_applicable="clinical_withdrawal_reason",
        )

        self.validate_other_specify(
            other_stored_value=INVESTIGATOR_DECISION,
            field="clinical_withdrawal_reason",
            other_specify_field="clinical_withdrawal_investigator_decision",
        )

        self.validate_other_specify(
            field="clinical_withdrawal_reason",
            other_specify_field="clinical_withdrawal_reason_other",
        )

        self.required_if(
            CONSENT_WITHDRAWAL,
            field="offstudy_reason",
            field_required="consent_withdrawal_reason",
        )

    def validate_completed_36m(self):
        if (
            self.cleaned_data.get("offstudy_reason")
            and self.cleaned_data.get("offstudy_reason").name == COMPLETED_FOLLOWUP
        ):
            subject_visit_model_cls = django_apps.get_model("meta_subject.subjectvisit")
            try:
                subject_visit_model_cls.objects.get(
                    subject_identifier=self.subject_identifier,
                    visit_code=MONTH36,
                    visit_code_sequence=0,
                )
            except ObjectDoesNotExist:
                self.raise_validation_error(
                    {"offstudy_reason": "Invalid. 36 month visit has not been submitted."},
                    INVALID_ERROR,
                )

    def validate_pregnancy(self):
        if (
            self.cleaned_data.get("offstudy_reason")
            and self.cleaned_data.get("offstudy_reason").name == PREGNANCY
        ):
            delivery_model_cls = django_apps.get_model("meta_subject.delivery")
            pregnancy_notification_model_cls = django_apps.get_model(
                "meta_prn.pregnancynotification"
            )
            try:
                delivery_model_cls.objects.get(
                    subject_visit__subject_identifier=self.subject_identifier,
                )
            except ObjectDoesNotExist:
                pass
            else:
                self.raise_validation_error(
                    {
                        "offstudy_reason": (
                            f"Invalid. {delivery_model_cls._meta.verbose_name} "
                            "has been submitted."
                        )
                    },
                    INVALID_ERROR,
                )
            try:
                obj = pregnancy_notification_model_cls.objects.get(
                    subject_identifier=self.subject_identifier,
                )
            except ObjectDoesNotExist:
                self.raise_validation_error(
                    {
                        "offstudy_reason": (
                            f"Invalid. {pregnancy_notification_model_cls._meta.verbose_name} "
                            "has not been submitted."
                        )
                    },
                    INVALID_ERROR,
                )
            else:
                if (obj.bhcg_date or obj.report_datetime.date()) != self.cleaned_data.get(
                    "pregnancy_date"
                ):
                    dt = formatted_date((obj.bhcg_date or obj.report_datetime.date()))
                    self.raise_validation_error(
                        {
                            "pregnancy_date": (
                                "Invalid. Does not match date on "
                                f"{pregnancy_notification_model_cls._meta.verbose_name}. "
                                f"Expected {dt}."
                            )
                        },
                        INVALID_ERROR,
                    )

    def validate_delivery(self):
        if (
            self.cleaned_data.get("offstudy_reason")
            and self.cleaned_data.get("offstudy_reason").name == DELIVERY
        ):
            delivery_model_cls = django_apps.get_model("meta_subject.delivery")
            try:
                obj = delivery_model_cls.objects.get(
                    subject_visit__subject_identifier=self.subject_identifier,
                )
            except ObjectDoesNotExist:
                self.raise_validation_error(
                    {
                        "offstudy_reason": (
                            f"Invalid. {delivery_model_cls._meta.verbose_name} "
                            "has not been submitted."
                        )
                    },
                    INVALID_ERROR,
                )
            else:
                if (
                    obj.delivery_datetime.date() or obj.report_datetime.date()
                ) != self.cleaned_data.get("delivery_date"):
                    dt = formatted_date(
                        (obj.delivery_datetime.date() or obj.report_datetime.date())
                    )
                    self.raise_validation_error(
                        {
                            "delivery_date": (
                                "Invalid. Does not match date on "
                                f"{delivery_model_cls._meta.verbose_name}. "
                                f"Expected {dt}."
                            )
                        },
                        INVALID_ERROR,
                    )

    def validate_study_medication_status(self):
        off_study_medication_model_cls = django_apps.get_model("meta_prn.offstudymedication")
        try:
            off_study_medication_model_cls.objects.get(
                subject_identifier=self.subject_identifier
            )
        except ObjectDoesNotExist:
            action_type = ActionType.objects.get(name=OFFSTUDY_MEDICATION_ACTION)
            url = reverse("edc_action_item_admin:edc_action_item_actionitem_add")
            data = dict(
                subject_identifier=self.subject_identifier,
                action_type=str(action_type.id),
            )
            query_string = "&".join(
                [
                    "next=meta_dashboard:subject_dashboard_url,subject_identifier",
                    parse.urlencode(data),
                ]
            )

            self.raise_validation_error(
                format_html(
                    "Participant is reported to be on study medication. Complete "
                    f'<a href="{url}?{query_string}" title="Add new form">'
                    f"{off_study_medication_model_cls._meta.verbose_name}</A> "
                    "PRN action and try again."
                ),
                INVALID_ERROR,
            )

    def confirm_off_all_schedules(self):
        try:
            off_all_schedules_or_raise(
                subject_identifier=self.cleaned_data.get("subject_identifier"),
            )
        except OffstudyError as e:
            self.raise_validation_error(str(e), INVALID_ERROR)

    def validate_offstudy_datetime_against_last_seen_date(self):
        if self.cleaned_data.get("offstudy_datetime") and self.cleaned_data.get(
            "last_seen_date"
        ):
            if (
                self.cleaned_data.get("last_seen_date")
                > self.cleaned_data.get("offstudy_datetime").date()
            ):
                raise forms.ValidationError(
                    {"last_seen_date": "Invalid. May not be after termination date"}
                )

    def validate_transfer(self):
        if (
            self.cleaned_data.get("offstudy_reason")
            and self.cleaned_data.get("offstudy_reason").name == TRANSFERRED
        ):
            transfer_model_cls = django_apps.get_model("meta_prn.subjecttransfer")
            try:
                obj = transfer_model_cls.objects.get(
                    subject_visit__subject_identifier=self.subject_identifier,
                )
            except ObjectDoesNotExist:
                self.raise_validation_error(
                    {
                        "offstudy_reason": (
                            f"Invalid. {transfer_model_cls._meta.verbose_name} "
                            "has not been submitted."
                        )
                    },
                    INVALID_ERROR,
                )
            else:
                if obj.transfer_date.date() != self.cleaned_data.get("transfer_date"):
                    dt = formatted_date(obj.transfer_date)
                    self.raise_validation_error(
                        {
                            "transfer_date": (
                                "Invalid. Does not match date on "
                                f"{transfer_model_cls._meta.verbose_name}. Expected {dt}."
                            )
                        },
                        INVALID_ERROR,
                    )
