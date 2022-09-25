from django import forms
from edc_form_validators import FormValidatorMixin
from edc_offstudy.modelform_mixins import OffstudyNonCrfModelFormMixin
from edc_sites.forms import SiteModelFormMixin
from edc_visit_tracking.form_validators import VisitFormValidator
from edc_visit_tracking.modelform_mixins import VisitTrackingModelFormMixin

from ..models import SubjectVisit


class SubjectVisitFormValidator(VisitFormValidator):
    validate_missed_visit_reason = False


class SubjectVisitForm(
    SiteModelFormMixin,
    VisitTrackingModelFormMixin,
    OffstudyNonCrfModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):

    form_validator_cls = SubjectVisitFormValidator

    class Meta:
        model = SubjectVisit
        fields = "__all__"
