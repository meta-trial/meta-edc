from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import Sf12Form
from ..models import Sf12
from .modeladmin import CrfModelAdmin


@admin.register(Sf12, site=meta_subject_admin)
class Sf12Admin(CrfModelAdmin):

    form = Sf12Form

    additional_instructions = mark_safe(
        "<p>"
        "This survey asks for your views about your health. This information "
        "will help keep track of how you feel and how well you are able to do "
        "your usual activities. "
        "<b>Answer each question by choosing just one answer</b>. If you are "
        "unsure how to answer a question, please give the best answer you can."
        "</p>"
    )

    past_4w = "<u>past 4 weeks</u>"
    any_following_problems = (
        "have you had any of the following problems with your work or other "
        "regular daily activities"
    )

    part2_description = (
        "The following questions are about activities you might do during a typical day. "
        "Does <u>your health now limit you</u> in these activities? If so, how much?"
    )

    part3_description = (
        f"During the {past_4w}, {any_following_problems} "
        "<u>as a result of your physical health</u>?"
    )

    part4_description = (
        f"During the {past_4w}, {any_following_problems} "
        "<u>as a result of any emotional problems</u> (such as feeling depressed or anxious)?"
    )

    part6_description = (
        "<p>"
        f"These questions are about how you have been feeling during the {past_4w}. "
        "For each question, please give the one answer that comes closest to the "
        "way you have been feeling."
        "</p>"
        "<p>"
        f"How much of the time during the {past_4w}..."
        "</p>"
    )

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Part 1: General health",
            {"fields": ("general_health",)},
        ),
        (
            "Part 2: Activities limited by health",
            {
                "description": format_html(part2_description),
                "fields": (
                    "moderate_activities_now_limited",
                    "climbing_stairs_now_limited",
                ),
            },
        ),
        (
            "Part 3: Physical health problems (last 4 weeks)",
            {
                "description": format_html(part3_description),
                "fields": (
                    "accomplished_less_physical_health",
                    "work_limited_physical_health",
                ),
            },
        ),
        (
            "Part 4: Emotional problems (last 4 weeks)",
            {
                "description": format_html(part4_description),
                "fields": (
                    "accomplished_less_emotional",
                    "work_less_carefully_emotional",
                ),
            },
        ),
        (
            "Part 5: Pain (last 4 weeks)",
            {"fields": ("pain_interfere_work",)},
        ),
        (
            "Part 6: Feeling (last 4 weeks)",
            {
                "description": format_html(part6_description),
                "fields": (
                    "felt_calm_peaceful",
                    "felt_lot_energy",
                    "felt_down",
                ),
            },
        ),
        (
            "Part 7: Social activities (last 4 weeks)",
            {"fields": ("social_activities_interfered",)},
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "accomplished_less_emotional": admin.VERTICAL,
        "accomplished_less_physical_health": admin.VERTICAL,
        "climbing_stairs_now_limited": admin.VERTICAL,
        "felt_calm_peaceful": admin.VERTICAL,
        "felt_down": admin.VERTICAL,
        "felt_lot_energy": admin.VERTICAL,
        "general_health": admin.VERTICAL,
        "moderate_activities_now_limited": admin.VERTICAL,
        "pain_interfere_work": admin.VERTICAL,
        "social_activities_interfered": admin.VERTICAL,
        "work_less_carefully_emotional": admin.VERTICAL,
        "work_limited_physical_health": admin.VERTICAL,
    }
