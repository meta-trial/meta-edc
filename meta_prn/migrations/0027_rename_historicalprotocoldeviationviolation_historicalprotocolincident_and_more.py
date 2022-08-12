# Generated by Django 4.0.5 on 2022-06-25 20:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_protocol_violation", "0006_protocolincidents_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("edc_action_item", "0028_auto_20210203_0706"),
        ("sites", "0002_alter_domain_unique"),
        (
            "meta_prn",
            "0026_remove_historicalprotocoldeviationviolation_violation_type_and_more",
        ),
    ]

    operations = [
        migrations.RenameModel(
            old_name="HistoricalProtocolDeviationViolation",
            new_name="HistoricalProtocolIncident",
        ),
        migrations.RenameModel(
            old_name="ProtocolDeviationViolation",
            new_name="ProtocolIncident",
        ),
        migrations.RemoveIndex(
            model_name="protocolincident",
            name="meta_prn_pr_subject_6d4791_idx",
        ),
        migrations.AddIndex(
            model_name="protocolincident",
            index=models.Index(
                fields=["subject_identifier", "action_identifier", "site", "id"],
                name="meta_prn_pr_subject_e85b31_idx",
            ),
        ),
    ]
