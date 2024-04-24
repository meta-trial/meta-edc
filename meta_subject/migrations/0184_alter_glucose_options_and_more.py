# Generated by Django 5.0.4 on 2024-04-09 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0183_alter_dmfollowup_on_dm_medications_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="glucose",
            options={
                "default_manager_name": "objects",
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "verbose_name": "Glucose (FBG/RBG, OGTT)",
                "verbose_name_plural": "Glucose (FBG/RBG, OGTT)",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalglucose",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Glucose (FBG/RBG, OGTT)",
                "verbose_name_plural": "historical Glucose (FBG/RBG, OGTT)",
            },
        ),
    ]