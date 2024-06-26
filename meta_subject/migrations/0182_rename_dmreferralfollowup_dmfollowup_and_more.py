# Generated by Django 4.2.11 on 2024-04-04 14:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("edc_action_item", "0037_remove_actionitem_reference_model_and_more"),
        ("meta_lists", "0018_missedreferralreasons"),
        ("meta_subject", "0181_dmreferralfollowup_action_identifier_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DmReferralFollowup",
            new_name="DmFollowup",
        ),
        migrations.RenameModel(
            old_name="HistoricalDmReferralFollowup",
            new_name="HistoricalDmFollowup",
        ),
        migrations.AlterModelOptions(
            name="dmfollowup",
            options={
                "default_manager_name": "objects",
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "verbose_name": "Diabetes follow-up after referral",
                "verbose_name_plural": "Diabetes follow-up after referral",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaldmfollowup",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Diabetes follow-up after referral",
                "verbose_name_plural": "historical Diabetes follow-up after referral",
            },
        ),
        migrations.RenameIndex(
            model_name="dmfollowup",
            new_name="meta_subjec_subject_dd09d5_idx",
            old_name="meta_subjec_subject_cfb7da_idx",
        ),
        migrations.RenameIndex(
            model_name="dmfollowup",
            new_name="meta_subjec_subject_1313a7_idx",
            old_name="meta_subjec_subject_257846_idx",
        ),
    ]
