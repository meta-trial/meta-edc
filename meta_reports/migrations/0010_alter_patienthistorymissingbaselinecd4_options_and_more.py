# Generated by Django 5.0.7 on 2024-08-12 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0009_alter_endpoints_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="patienthistorymissingbaselinecd4",
            options={
                "default_permissions": ("view", "export", "viewallsites"),
                "managed": False,
                "verbose_name": "Patient History: Missing Baseline Cd4",
                "verbose_name_plural": "Missing Baseline Cd4",
            },
        ),
        migrations.AlterModelOptions(
            name="unattendedthreeinrow",
            options={
                "default_permissions": ("view", "export", "viewallsites"),
                "managed": False,
                "verbose_name": "R100: Unattended appointments: Three in a row",
                "verbose_name_plural": "R100: Unattended appointments: Three in a row",
            },
        ),
        migrations.AlterModelOptions(
            name="unattendedthreeinrow2",
            options={
                "default_permissions": ("view", "export", "viewallsites"),
                "managed": False,
                "verbose_name": "R110: Unattended appointments: Three in a row (with missed)",
                "verbose_name_plural": "R110: Unattended appointments: Three in a row (with missed)",
            },
        ),
        migrations.AlterModelOptions(
            name="unattendedtwoinrow",
            options={
                "default_permissions": ("view", "export", "viewallsites"),
                "managed": False,
                "verbose_name": "R120: Unattended appointments: Two in a row",
                "verbose_name_plural": "R120: Unattended appointments: Two in a row",
            },
        ),
    ]