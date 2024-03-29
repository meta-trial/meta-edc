# Generated by Django 5.0.1 on 2024-02-14 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0172_remove_historicalbloodresultsglu_action_item_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="glucosefbg",
            name="action_identifier",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="action_item",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="action_item_reason",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="missing",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="missing_count",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="parent_action_identifier",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="parent_action_item",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="related_action_identifier",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="related_action_item",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="requisition",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="results_abnormal",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="results_reportable",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="summary",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="action_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="action_item",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="action_item_reason",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="missing",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="missing_count",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="parent_action_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="parent_action_item",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="related_action_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="related_action_item",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="requisition",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="results_abnormal",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="results_reportable",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="summary",
        ),
    ]
