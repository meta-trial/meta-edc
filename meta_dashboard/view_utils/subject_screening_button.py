from __future__ import annotations

from dataclasses import dataclass, field
from typing import Type

from django.utils.translation import gettext as _
from edc_constants.constants import TBD, YES
from edc_subject_dashboard.view_utils import ADD, CHANGE, VIEW
from edc_subject_dashboard.view_utils.subject_screening_button import (
    SubjectScreeningButton as BaseSubjectScreeningButton,
)

from meta_screening.models import ScreeningPartOne, ScreeningPartThree, ScreeningPartTwo

__all__ = [
    "SubjectScreeningPartOneButton",
    "SubjectScreeningPartTwoButton",
    "SubjectScreeningPartThreeButton",
]


@dataclass
class SubjectScreeningButton(BaseSubjectScreeningButton):
    next_url_name: str = field(default="screening_listboard_url")

    def __post_init__(self):
        self.model_obj = self.model_cls.objects.get(
            screening_identifier=self.model_obj.screening_identifier
        )

    @property
    def label(self) -> str:
        return "P1"

    @property
    def color(self) -> str:
        return self.colors[self.action]

    @property
    def title(self) -> str:
        if self.perms.view_only or self.model_obj.consented:
            title = _("View")
        else:
            title = _("Edit")
        return title


@dataclass
class SubjectScreeningPartOneButton(SubjectScreeningButton):
    model_obj: ScreeningPartOne = None
    model_cls: Type[ScreeningPartOne] = field(default=ScreeningPartOne)

    @property
    def label(self) -> str:
        return "P1"


@dataclass
class SubjectScreeningPartTwoButton(SubjectScreeningButton):
    model_obj: ScreeningPartTwo = None
    model_cls: Type[ScreeningPartTwo] = field(default=ScreeningPartTwo)

    @property
    def label(self) -> str:
        return "P2"

    @property
    def color(self) -> str:
        if self.action == ADD and self.disabled:
            return "default"
        return self.colors[self.action]

    @property
    def action(self):
        if not self._action:
            self._action = VIEW
            if self.model_obj.eligible_part_two == TBD:
                self._action = ADD
            elif self.model_obj:
                if self.perms.change:
                    self._action = CHANGE
        return self._action

    @property
    def disabled(self) -> str:
        if self.model_obj.eligible_part_one == YES and self.model_obj.continue_part_two == YES:
            return ""
        return "disabled"


@dataclass
class SubjectScreeningPartThreeButton(SubjectScreeningButton):
    model_obj: ScreeningPartThree = None
    model_cls: Type[ScreeningPartThree] = field(default=ScreeningPartThree)

    @property
    def label(self) -> str:
        return "P3"

    @property
    def color(self) -> str:
        if self.action == ADD and self.disabled:
            return "default"
        return self.colors[self.action]

    @property
    def action(self):
        if not self._action:
            self._action = VIEW
            if self.model_obj.eligible_part_three == TBD:
                self._action = ADD
            elif self.model_obj:
                if self.perms.change:
                    self._action = CHANGE
        return self._action

    @property
    def disabled(self) -> str:
        if self.model_obj.eligible_part_one == YES and self.model_obj.eligible_part_two == YES:
            return ""
        return "disabled"
