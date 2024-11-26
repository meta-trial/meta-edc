# Generated by Django 5.0.8 on 2024-08-28 19:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edc_action_item", "0037_remove_actionitem_reference_model_and_more"),
        ("meta_subject", "0212_auto_20240827_2222"),
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="BloodResultsLipid",
            new_name="BloodResultsLipids",
        ),
        migrations.RenameModel(
            old_name="HistoricalBloodResultsLipid",
            new_name="HistoricalBloodResultsLipids",
        ),
        migrations.RenameIndex(
            model_name="bloodresultslipids",
            new_name="meta_subjec_subject_eff3e6_idx",
            old_name="meta_subjec_subject_296de9_idx",
        ),
        migrations.RenameIndex(
            model_name="bloodresultslipids",
            new_name="meta_subjec_subject_49b971_idx",
            old_name="meta_subjec_subject_9692a2_idx",
        ),
    ]