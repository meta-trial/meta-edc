# Generated by Django 3.2.11 on 2022-03-09 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_prn", "0018_auto_20220309_2106"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="birthoutcomes",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ["subject_identifier", "birth_order"],
                "verbose_name": "Birth Outcomes",
                "verbose_name_plural": "Birth Outcomes",
            },
        ),
        migrations.RenameField(
            model_name="birthoutcomes",
            old_name="maternal_identifier",
            new_name="subject_identifier",
        ),
        migrations.RenameField(
            model_name="historicalbirthoutcomes",
            old_name="maternal_identifier",
            new_name="subject_identifier",
        ),
        migrations.AlterUniqueTogether(
            name="birthoutcomes",
            unique_together={("subject_identifier", "birth_order")},
        ),
    ]
