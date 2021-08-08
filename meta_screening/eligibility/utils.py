from django.utils.html import format_html


def format_reasons_ineligible(*str_values):
    reasons = None
    str_values = [x for x in str_values if x is not None]
    if str_values:
        str_values = "".join(str_values)
        reasons = format_html(str_values.replace("|", "<BR>"))
    return reasons
