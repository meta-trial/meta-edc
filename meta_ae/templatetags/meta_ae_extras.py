import arrow

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from edc_constants.constants import OTHER, YES
from textwrap import wrap

register = template.Library()


format_ae_description_template_name = (
    f"{settings.ADVERSE_EVENT_APP_LABEL}/bootstrap{settings.EDC_BOOTSTRAP}/"
    f"ae_initial_description.html"
)


@register.inclusion_tag(format_ae_description_template_name, takes_context=True)
def format_ae_description(context, ae_initial, wrap_length):
    context["utc_date"] = arrow.now().date()
    context["SHORT_DATE_FORMAT"] = settings.SHORT_DATE_FORMAT
    context["OTHER"] = OTHER
    context["YES"] = YES
    context["ae_initial"] = ae_initial
    context["sae_reason"] = mark_safe(
        "<BR>".join(wrap(ae_initial.sae_reason.name, wrap_length or 35))
    )
    context["ae_description"] = mark_safe(
        "<BR>".join(wrap(ae_initial.ae_description, wrap_length or 35))
    )
    return context
