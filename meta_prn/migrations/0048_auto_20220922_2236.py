# Generated by Django 3.2.13 on 2022-09-22 19:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_pharmacy", "0015_auto_20220913_2139"),
        ("meta_prn", "0047_auto_20220826_0406"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="offschedule",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Off-schedule",
                "verbose_name_plural": "Off-schedule",
            },
        ),
        migrations.AlterModelOptions(
            name="offschedulepostnatal",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Off-schedule: post-natal",
                "verbose_name_plural": "Off-schedule: post-natal",
            },
        ),
        migrations.AlterModelOptions(
            name="offschedulepregnancy",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Off-schedule: Pregnancy",
                "verbose_name_plural": "Off-schedule: Pregnancy",
            },
        ),
        migrations.AlterModelOptions(
            name="onschedule",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
            },
        ),
        migrations.AlterModelOptions(
            name="onschedulepregnancy",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
            },
        ),
        migrations.AddField(
            model_name="offstudymedication",
            name="medications",
            field=models.ManyToManyField(
                limit_choices_to={"name": "metformin"}, to="edc_pharmacy.Medication"
            ),
        ),
    ]
