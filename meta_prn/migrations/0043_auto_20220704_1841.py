# Generated by Django 3.2.13 on 2022-07-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_prn", "0042_remove_endofstudy_investigator_decision_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicalendofstudy",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical End of Study",
                "verbose_name_plural": "historical End of Study",
            },
        ),
        migrations.AlterModelOptions(
            name="historicallosstofollowup",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Loss to Follow Up",
                "verbose_name_plural": "historical Loss to Follow Up",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaloffschedule",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Off-schedule",
                "verbose_name_plural": "historical Off-schedule",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaloffschedulepostnatal",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Off-schedule: post-natal",
                "verbose_name_plural": "historical Off-schedule: post-natal",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaloffschedulepregnancy",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Off-schedule: Pregnancy",
                "verbose_name_plural": "historical Off-schedule: Pregnancy",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaloffstudymedication",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Withdrawal of Study Drug",
                "verbose_name_plural": "historical Withdrawal of Study Drug",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalonschedule",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical on schedule",
                "verbose_name_plural": "historical on schedules",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalonschedulepostnatal",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical on schedule postnatal",
                "verbose_name_plural": "historical on schedule postnatals",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalonschedulepregnancy",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical on schedule pregnancy",
                "verbose_name_plural": "historical on schedule pregnancys",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalpregnancynotification",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Pregnancy Notification",
                "verbose_name_plural": "historical Pregnancy Notifications",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalprotocolincident",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Protocol Incident",
                "verbose_name_plural": "historical Protocol Incident",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalsubjecttransfer",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Subject Transfer",
                "verbose_name_plural": "historical Subject Transfers",
            },
        ),
        migrations.AlterField(
            model_name="historicalendofstudy",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicallosstofollowup",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicaloffschedule",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicaloffschedulepostnatal",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicaloffschedulepregnancy",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicaloffstudymedication",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalonschedule",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalonschedulepostnatal",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalonschedulepregnancy",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalpregnancynotification",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalprotocolincident",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalsubjecttransfer",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
    ]
