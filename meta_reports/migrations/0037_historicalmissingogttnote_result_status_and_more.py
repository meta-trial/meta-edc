# Generated by Django 5.0.8 on 2024-08-23 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0036_historicalmissingogttnote_fasting_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalmissingogttnote",
            name="result_status",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=25,
                verbose_name="Is the OGTT result available",
            ),
        ),
        migrations.AddField(
            model_name="missingogttnote",
            name="result_status",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=25,
                verbose_name="Is the OGTT result available",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmissingogttnote",
            name="status",
            field=models.CharField(
                choices=[("COMPLETE", "Complete"), ("not_available", "Not available")],
                default="done",
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name="missingogttnote",
            name="status",
            field=models.CharField(
                choices=[("COMPLETE", "Complete"), ("not_available", "Not available")],
                default="done",
                max_length=25,
            ),
        ),
    ]