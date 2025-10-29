from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from clinicedc_constants import TBD
from django import template
from edc_dashboard.url_names import url_names

from meta_consent.models import SubjectConsent
from meta_dashboard.view_utils import (
    SubjectScreeningPartOneButton,
    SubjectScreeningPartThreeButton,
    SubjectScreeningPartTwoButton,
)
from meta_screening.eligibility import get_display_label
from meta_screening.models import (
    ScreeningPartOne,
    ScreeningPartThree,
    ScreeningPartTwo,
    SubjectScreening,
)

if TYPE_CHECKING:
    pass


register = template.Library()


@register.inclusion_tag("meta_dashboard/buttons/eligibility_button.html")
def eligibility_button(subject_screening: SubjectScreening):
    comment = []
    tooltip = None
    if subject_screening.reasons_ineligible:
        comment = subject_screening.reasons_ineligible.split("|")
        comment = list(set(comment))
        comment.sort()
    display_label = get_display_label(subject_screening)
    soup = BeautifulSoup(display_label, features="html.parser")
    return dict(
        eligible=subject_screening.eligible,
        eligible_final=subject_screening.eligible,
        display_label=soup.get_text(),
        comment=comment,
        tooltip=tooltip,
        TBD=TBD,
    )


@register.inclusion_tag(
    "meta_dashboard/buttons/add_consent_button.html",
    takes_context=True,
)
def render_consent_button(context, subject_screening: SubjectScreening):
    title = ["Consent subject to participate."]
    cdef = subject_screening.consent_definition
    return dict(
        perms=context["perms"],
        screening_identifier=subject_screening.screening_identifier,
        # href=model_wrapper.consent.href,
        consent_version=cdef.version,
        title=" ".join(title),
    )


def refusal_button(context, subject_refusal):  # noqa: ARG001
    title = ["Capture subject's primary reason for not joining."]

    return dict(
        perms=context["perms"],
        # href=subject_refusal_model_wrapper.href,
        title=" ".join(title),
    )


@register.inclusion_tag("edc_listboard/buttons/dashboard_button.html")
def render_dashboard_button(subject_consent: SubjectConsent):
    subject_dashboard_url = url_names.get("subject_dashboard_url")
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=subject_consent.subject_identifier,
    )


@register.inclusion_tag(
    "edc_subject_dashboard/buttons/forms_button.html",
    takes_context=True,
)
def render_screening_part_one_button(context, subject_screening: ScreeningPartOne) -> dict:
    btn = SubjectScreeningPartOneButton(
        user=context["request"].user,
        model_obj=subject_screening,
        current_site=context["request"].site,
    )
    return dict(btn=btn)


@register.inclusion_tag(
    "edc_subject_dashboard/buttons/forms_button.html",
    takes_context=True,
)
def render_screening_part_two_button(context, subject_screening: ScreeningPartTwo) -> dict:
    btn = SubjectScreeningPartTwoButton(
        user=context["request"].user,
        model_obj=subject_screening,
        current_site=context["request"].site,
    )
    return dict(btn=btn)


@register.inclusion_tag(
    "edc_subject_dashboard/buttons/forms_button.html",
    takes_context=True,
)
def render_screening_part_three_button(context, subject_screening: ScreeningPartThree) -> dict:
    btn = SubjectScreeningPartThreeButton(
        user=context["request"].user,
        model_obj=subject_screening,
        current_site=context["request"].site,
    )
    return dict(btn=btn)
