# Generated by Django 4.2.11 on 2024-07-27 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("meta_reports", "0004_alter_patienthistorymissingbaselinecd4_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="Endpoints",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("report_model", models.CharField(max_length=50)),
                ("subject_identifier", models.CharField(max_length=25)),
                ("created", models.DateTimeField()),
                ("visit_code", models.IntegerField()),
                ("fasting", models.CharField(max_length=10)),
                ("fbg_datetime", models.DateTimeField()),
                ("fbg_value", models.FloatField()),
                ("ogtt_value", models.FloatField()),
                ("endpoint_label", models.CharField(max_length=25)),
                ("offstudy_datetime", models.DateTimeField(null=True)),
                ("offstudy_reason", models.CharField(max_length=250, null=True)),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="sites.site"
                    ),
                ),
            ],
            options={
                "verbose_name": "Endpoints (DM)",
                "verbose_name_plural": "Endpoints (DM)",
            },
        ),
    ]
