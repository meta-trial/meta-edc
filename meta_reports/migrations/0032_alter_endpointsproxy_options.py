# Generated by Django 5.0.8 on 2024-08-22 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0031_endpointsproxy"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="endpointsproxy",
            options={
                "default_permissions": ("view", "export", "viewallsites"),
                "verbose_name": "Endpoints (DM): All",
                "verbose_name_plural": "Endpoints (DM): All",
            },
        ),
    ]
