# Generated by Django 3.2.11 on 2022-07-22 01:11
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from edc_action_item.identifiers import ActionIdentifier
from edc_constants.constants import CLOSED, HIGH_PRIORITY
from tqdm import tqdm

from meta_subject.constants import MISSED_VISIT_ACTION


def update_missing_action_items_for_missed_visits(apps, schema_editor):
    actiontype_model_cls = apps.get_model("edc_action_item.actiontype")
    actionitem_model_cls = apps.get_model("edc_action_item.actionitem")
    subjectvisitmissed_model_cls = apps.get_model("meta_subject.subjectvisitmissed")
    subjectvisit_model_cls = apps.get_model("meta_subject.subjectvisit")
    try:
        action_type = actiontype_model_cls.objects.get(name=MISSED_VISIT_ACTION)
    except ObjectDoesNotExist:
        pass
    else:
        total = subjectvisitmissed_model_cls.objects.filter(
            action_identifier__isnull=True
        ).count()
        for obj in tqdm(
            subjectvisitmissed_model_cls.objects.filter(action_identifier__isnull=True),
            total=total,
        ):
            subject_visit = subjectvisit_model_cls.objects.get(id=obj.subject_visit_id)
            action_item = actionitem_model_cls.objects.create(
                subject_identifier=subject_visit.subject_identifier,
                action_identifier=ActionIdentifier(site_id=subject_visit.site_id).identifier,
                report_datetime=subject_visit.report_datetime,
                action_type=action_type,
                reference_model="meta_subject.subjectvisitmissed",
                linked_to_reference=True,
                priority=HIGH_PRIORITY,
                status=CLOSED,
                auto_created=True,
                site_id=subject_visit.site_id,
            )
            obj.action_identifier = action_item.action_identifier
            obj.save_base(update_fields=["action_identifier"])


class Migration(migrations.Migration):
    dependencies = [
        ("meta_subject", "0130_auto_20220720_0216"),
    ]

    operations = [migrations.RunPython(update_missing_action_items_for_missed_visits)]
