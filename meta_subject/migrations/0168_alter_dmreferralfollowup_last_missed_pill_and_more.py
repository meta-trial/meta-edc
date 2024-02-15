# Generated by Django 5.0.1 on 2024-02-13 01:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "meta_subject",
            "0167_rename_healthcare_workers_other_dmreferralfollowup_other_healthcare_workers_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="dmreferralfollowup",
            name="last_missed_pill",
            field=models.CharField(
                blank=True,
                choices=[
                    ("today", "today"),
                    ("yesterday", "yesterday"),
                    ("earlier_this_week", "earlier this week"),
                    ("last_week", "last week"),
                    ("lt_month_ago", "less than a month ago"),
                    ("gt_month_ago", "more than a month ago"),
                    ("NEVER", "have never missed taking my study pills"),
                ],
                max_length=25,
                null=True,
                verbose_name="When was the last time you missed your study pill?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldmreferralfollowup",
            name="last_missed_pill",
            field=models.CharField(
                blank=True,
                choices=[
                    ("today", "today"),
                    ("yesterday", "yesterday"),
                    ("earlier_this_week", "earlier this week"),
                    ("last_week", "last week"),
                    ("lt_month_ago", "less than a month ago"),
                    ("gt_month_ago", "more than a month ago"),
                    ("NEVER", "have never missed taking my study pills"),
                ],
                max_length=25,
                null=True,
                verbose_name="When was the last time you missed your study pill?",
            ),
        ),
    ]
