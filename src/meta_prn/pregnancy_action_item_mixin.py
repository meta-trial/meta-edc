from __future__ import annotations

from typing import TYPE_CHECKING

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_visit_schedule.constants import OFFSCHEDULE_ACTION

from .constants import OFFSCHEDULE_PREGNANCY_ACTION

if TYPE_CHECKING:
    from .models import OffSchedulePregnancy


class PregnancyActionItemMixin:
    """A mixin for off schedule action items"""

    def get_next_offschedule_action(self) -> str:
        """Returns next off schedule action name.

        Called by get_next_actions().
        """
        try:
            self.offschedule_pregnancy_model_cls.objects.get(
                subject_identifier=self.subject_identifier
            )
        except ObjectDoesNotExist:
            return OFFSCHEDULE_ACTION
        else:
            return OFFSCHEDULE_PREGNANCY_ACTION

    @property
    def offschedule_pregnancy_model_cls(self) -> OffSchedulePregnancy:
        return django_apps.get_model("meta_prn.offschedulepregnancy")
