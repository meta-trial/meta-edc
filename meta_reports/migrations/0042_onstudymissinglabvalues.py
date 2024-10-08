# Generated by Django 5.0.8 on 2024-08-28 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0041_auto_20240828_2229"),
    ]

    operations = [
        migrations.CreateModel(
            name="OnStudyMissingLabValues",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("original_id", models.UUIDField(null=True)),
                ("label_lower", models.CharField(max_length=150, null=True)),
                ("subject_visit_id", models.UUIDField(null=True)),
                ("report_datetime", models.DateTimeField(null=True)),
                ("label", models.CharField(max_length=50, null=True)),
                ("visit_code", models.CharField(max_length=25, null=True)),
                ("visit_code_sequence", models.IntegerField(null=True)),
                ("schedule_name", models.CharField(max_length=25, null=True)),
                ("modified", models.DateTimeField(null=True)),
                ("report_model", models.CharField(max_length=50)),
                ("subject_identifier", models.CharField(max_length=25)),
                ("created", models.DateTimeField()),
            ],
            options={
                "verbose_name": "Missing Lab values for on-study patient",
                "verbose_name_plural": "Missing Lab values for on-study patients",
                "db_table": "onstudy_missing_lab_values_view",
                "managed": False,
                "default_permissions": ("view", "export", "viewallsites"),
            },
        ),
    ]
