from bs4 import BeautifulSoup
from django import template
from edc_constants.constants import NO, TBD, YES
from edc_dashboard.url_names import url_names
from edc_dashboard.utils import get_bootstrap_version

from meta_screening.eligibility import get_display_label

register = template.Library()


@register.inclusion_tag(
    f"meta_dashboard/bootstrap{get_bootstrap_version()}/" f"buttons/screening_button.html",
    takes_context=True,
)
def screening_button(context, model_wrapper):
    title = "Edit subject's screening form"
    perms = context["perms"]

    p1 = model_wrapper.object.eligible_part_one

    continue_p2 = YES
    if (
        model_wrapper.object.eligible_part_one == NO
        and model_wrapper.object.continue_part_two == NO
    ):
        continue_p2 = NO

    p2 = model_wrapper.object.eligible_part_two
    p3 = model_wrapper.object.eligible_part_three
    p1_enabled = perms.user.has_perm(
        "meta_screening.view_screeningpartone"
    ) or perms.user.has_perm("meta_screening.change_screeningpartone")
    p2_enabled = (
        perms.user.has_perm("meta_screening.view_screeningparttwo")
        or perms.user.has_perm("meta_screening.change_screeningparttwo")
    ) and p1 in [YES, NO]
    p3_enabled = (
        (
            perms.user.has_perm("meta_screening.view_screeningparttwo")
            or perms.user.has_perm("meta_screening.change_screeningparttwo")
        )
        and p1 == YES
        and p2 == YES
    )
    return dict(
        continue_p2=continue_p2,
        perms=context["perms"],
        screening_identifier=model_wrapper.object.screening_identifier,
        href_p1=model_wrapper.href_p1,
        href_p2=model_wrapper.href_p2,
        href_p3=model_wrapper.href_p3,
        p1=p1,
        p2=p2,
        p3=p3,
        p1_enabled=p1_enabled,
        p2_enabled=None if continue_p2 == NO else p2_enabled,
        p3_enabled=p3_enabled,
        title=title,
        YES=YES,
        NO=NO,
        TBD=TBD,
    )


@register.inclusion_tag(
    f"meta_dashboard/bootstrap{get_bootstrap_version()}/" f"buttons/eligibility_button.html"
)
def eligibility_button(subject_screening_model_wrapper):
    comment = []
    obj = subject_screening_model_wrapper.object
    tooltip = None
    if obj.reasons_ineligible:
        comment = obj.reasons_ineligible.split("|")
        comment = list(set(comment))
        comment.sort()
    display_label = get_display_label(obj)
    soup = BeautifulSoup(display_label, features="html.parser")
    return dict(
        eligible=obj.eligible,
        eligible_final=obj.eligible,
        display_label=soup.get_text(),
        comment=comment,
        tooltip=tooltip,
        TBD=TBD,
    )


@register.inclusion_tag(
    f"meta_dashboard/bootstrap{get_bootstrap_version()}/buttons/add_consent_button.html",
    takes_context=True,
)
def add_consent_button(context, model_wrapper):
    title = ["Consent subject to participate."]
    consent_version = model_wrapper.consent.version
    return dict(
        perms=context["perms"],
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.consent.href,
        consent_version=consent_version,
        title=" ".join(title),
    )


def refusal_button(context, subject_refusal_model_wrapper):
    title = ["Capture subject's primary reason for not joining."]

    return dict(
        perms=context["perms"],
        href=subject_refusal_model_wrapper.href,
        title=" ".join(title),
    )


@register.inclusion_tag(
    f"meta_dashboard/bootstrap{get_bootstrap_version()}/" f"buttons/dashboard_button.html"
)
def dashboard_button(model_wrapper):
    subject_dashboard_url = url_names.get("subject_dashboard_url")
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier,
    )
