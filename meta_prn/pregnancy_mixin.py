from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .constants import OFFSCHEDULE_ACTION, OFFSCHEDULE_PREGNANCY_ACTION


class PregnancyMixin:
    """A mixin for off schedule action items"""

    @property
    def offschedule_pregnancy_model_cls(self):
        return django_apps.get_model("meta_prn.offschedulepregnancy")

    def get_next_offschedule_action(self):
        """Returns next off schedule action name"""
        try:
            self.offschedule_pregnancy_model_cls.objects.get(
                subject_identifier=self.subject_identifier
            )
        except ObjectDoesNotExist:
            return OFFSCHEDULE_ACTION
        else:
            return OFFSCHEDULE_PREGNANCY_ACTION
