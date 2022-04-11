from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_consent import ConsentModelWrapperMixin
from edc_constants.constants import PENDING
from edc_model_wrapper import ModelWrapper
from edc_subject_model_wrappers import SubjectConsentModelWrapper as BaseModelWrapper
from edc_utils import get_utcnow


class SubjectConsentModelWrapper(BaseModelWrapper):
    @property
    def querystring(self):
        return (
            f"cancel=meta_dashboard:screening_listboard_url,"
            f"screening_identifier&{super().querystring}"
        )


class SubjectScreeningModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    consent_model_wrapper_cls = SubjectConsentModelWrapper
    model = "meta_screening.subjectscreening"
    next_url_attrs = ["screening_identifier"]
    next_url_name = "screening_listboard_url"
    querystring_attrs = ["gender"]

    @property
    def create_consent_options(self):
        options = super().create_consent_options
        options.update(screening_identifier=self.object.screening_identifier)
        return options

    @property
    def consent_options(self):
        return dict(screening_identifier=self.object.screening_identifier)

    @property
    def consent_model_obj(self):
        consent_model_cls = django_apps.get_model(self.consent_model_wrapper_cls.model)
        try:
            return consent_model_cls.objects.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def human_screening_identifier(self):
        human = None
        if self.screening_identifier:
            human = f"{self.screening_identifier[0:4]}-{self.screening_identifier[4:]}"
        return human or self.screening_identifier

    @property
    def href_p1(self):
        return self.href.replace("subjectscreening", "screeningpartone")

    @property
    def href_p2(self):
        return self.href.replace("subjectscreening", "screeningparttwo")

    @property
    def href_p3(self):
        return self.href.replace("subjectscreening", "screeningpartthree")

    @property
    def repeat_due_in_days(self):
        if self.repeat_glucose_performed == PENDING and self.object.ogtt_datetime:
            return (get_utcnow() - self.object.ogtt_datetime).days
        return 0


class ScreeningPartOneModelWrapper(SubjectScreeningModelWrapper):

    model = "meta_screening.screeningpartone"

    @property
    def href_p1(self):
        return self.href

    @property
    def href_p2(self):
        return self.href.replace("screeningpartone", "screeningparttwo")

    @property
    def href_p3(self):
        return self.href.replace("screeningpartone", "screeningpartthree")
