# Generated by Django 5.0 on 2024-01-09 23:21

import edc_model.validators.date
import edc_protocol.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "edc_action_item",
            "0035_alter_actionitem_options_alter_actiontype_options_and_more",
        ),
        ("edc_adverse_event", "0014_alter_aeactionclassification_options_and_more"),
        ("meta_ae", "0019_alter_aefollowup_managers_alter_aeinitial_managers_and_more"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="aesusar",
            options={
                "verbose_name": "AE SUSAR Report",
                "verbose_name_plural": "AE SUSAR Reports",
            },
        ),
        migrations.AlterModelOptions(
            name="aetmg",
            options={
                "verbose_name": "AE TMG Report",
                "verbose_name_plural": "AE TMG Reports",
            },
        ),
        migrations.AlterModelOptions(
            name="deathreport",
            options={
                "verbose_name": "Death Report",
                "verbose_name_plural": "Death Reports",
            },
        ),
        migrations.RemoveIndex(
            model_name="aeinitial",
            name="meta_ae_aei_subject_9fefa3_idx",
        ),
        migrations.AddField(
            model_name="aefollowup",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="aefollowup",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="aeinitial",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="aeinitial",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="aelocalreview",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="aelocalreview",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="aesponsorreview",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="aesponsorreview",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="aesusar",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="aesusar",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="aetmg",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="aetmg",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="deathreport",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="deathreport",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="deathreporttmg",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="deathreporttmg",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="historicalaefollowup",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicalaefollowup",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="historicalaeinitial",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicalaeinitial",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="historicalaesusar",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicalaesusar",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="historicalaetmg",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicalaetmg",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreporttmg",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreporttmg",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreporttmgsecond",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreporttmgsecond",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AlterField(
            model_name="deathreport",
            name="death_date",
            field=models.DateField(
                null=True,
                validators=[
                    edc_protocol.validators.date_not_before_study_start,
                    edc_model.validators.date.date_not_future,
                ],
                verbose_name="Date of Death",
            ),
        ),
        migrations.AlterField(
            model_name="deathreport",
            name="death_datetime",
            field=models.DateTimeField(
                null=True,
                validators=[
                    edc_protocol.validators.datetime_not_before_study_start,
                    edc_model.validators.date.datetime_not_future,
                ],
                verbose_name="Date and Time of Death",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeathreport",
            name="death_date",
            field=models.DateField(
                null=True,
                validators=[
                    edc_protocol.validators.date_not_before_study_start,
                    edc_model.validators.date.date_not_future,
                ],
                verbose_name="Date of Death",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeathreport",
            name="death_datetime",
            field=models.DateTimeField(
                null=True,
                validators=[
                    edc_protocol.validators.datetime_not_before_study_start,
                    edc_model.validators.date.datetime_not_future,
                ],
                verbose_name="Date and Time of Death",
            ),
        ),
        migrations.AddIndex(
            model_name="aefollowup",
            index=models.Index(
                fields=["subject_identifier"], name="meta_ae_aef_subject_054161_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="aefollowup",
            index=models.Index(
                fields=[
                    "action_identifier",
                    "action_item",
                    "related_action_item",
                    "parent_action_item",
                ],
                name="meta_ae_aef_action__b2479a_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="aeinitial",
            index=models.Index(
                fields=["subject_identifier"], name="meta_ae_aei_subject_5e81f2_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="aeinitial",
            index=models.Index(
                fields=[
                    "action_identifier",
                    "action_item",
                    "related_action_item",
                    "parent_action_item",
                ],
                name="meta_ae_aei_action__8e0b23_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="aeinitial",
            index=models.Index(
                fields=["subject_identifier", "action_identifier", "site"],
                name="meta_ae_aei_subject_361c43_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="aesusar",
            index=models.Index(
                fields=["subject_identifier"], name="meta_ae_aes_subject_b8259b_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="aesusar",
            index=models.Index(
                fields=[
                    "action_identifier",
                    "action_item",
                    "related_action_item",
                    "parent_action_item",
                ],
                name="meta_ae_aes_action__ae027e_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="aetmg",
            index=models.Index(
                fields=["subject_identifier"], name="meta_ae_aet_subject_9a33b1_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="aetmg",
            index=models.Index(
                fields=[
                    "action_identifier",
                    "action_item",
                    "related_action_item",
                    "parent_action_item",
                ],
                name="meta_ae_aet_action__d28be4_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="deathreport",
            index=models.Index(
                fields=[
                    "action_identifier",
                    "action_item",
                    "related_action_item",
                    "parent_action_item",
                ],
                name="meta_ae_dea_action__4c8369_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="deathreporttmg",
            index=models.Index(
                fields=["subject_identifier"], name="meta_ae_dea_subject_910d26_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="deathreporttmg",
            index=models.Index(
                fields=[
                    "action_identifier",
                    "action_item",
                    "related_action_item",
                    "parent_action_item",
                ],
                name="meta_ae_dea_action__ea8160_idx",
            ),
        ),
    ]
