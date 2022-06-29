from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_constants.constants import NOT_APPLICABLE

from meta_screening.models import ScreeningPartThree


@receiver(
    post_save,
    weak=False,
    sender=ScreeningPartThree,
    dispatch_uid="update_p3_ltfu_on_post_save",
)
def update_p3_ltfu_on_post_save(sender, instance, raw, created, **kwargs):
    """ """
    if not raw:
        if instance.p3_ltfu != NOT_APPLICABLE and instance.part_three_report_datetime:
            msg = "[auto-updated p3 submitted]"
            instance.p3_ltfu = NOT_APPLICABLE
            instance.p3_ltfu_date = None
            instance.p3_ltfu_comment = (
                f"{msg} {instance.p3_ltfu_comment.replace(msg, '') or ''}".strip()
            )
            instance.save_base(update_fields=["p3_ltfu", "p3_ltfu_date", "p3_ltfu_comment"])
