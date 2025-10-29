from clinicedc_constants import NOT_APPLICABLE, NULL_STRING
from django.db.models.signals import post_save
from django.dispatch import receiver

from .proxy_models import ScreeningPartThree


@receiver(
    post_save,
    weak=False,
    sender=ScreeningPartThree,
    dispatch_uid="update_p3_ltfu_on_post_save",
)
def update_p3_ltfu_on_post_save(sender, instance, raw, created, **kwargs):  # noqa: ARG001
    """ """
    if not raw and instance.p3_ltfu != NOT_APPLICABLE and instance.part_three_report_datetime:
        msg = "[auto-updated p3 submitted]"
        instance.p3_ltfu = NOT_APPLICABLE
        instance.p3_ltfu_date = None
        instance.p3_ltfu_comment = (
            f"{msg} {instance.p3_ltfu_comment.replace(msg, NULL_STRING) or NULL_STRING}"
        ).strip()
        instance.save_base(update_fields=["p3_ltfu", "p3_ltfu_date", "p3_ltfu_comment"])
