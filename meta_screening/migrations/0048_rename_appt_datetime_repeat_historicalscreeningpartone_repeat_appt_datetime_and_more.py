# Generated by Django 4.0.5 on 2022-06-27 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta_screening', '0047_historicalscreeningpartone_appt_datetime_repeat_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalscreeningpartone',
            old_name='appt_datetime_repeat',
            new_name='repeat_appt_datetime',
        ),
        migrations.RenameField(
            model_name='historicalscreeningpartthree',
            old_name='appt_datetime_repeat',
            new_name='repeat_appt_datetime',
        ),
        migrations.RenameField(
            model_name='historicalscreeningparttwo',
            old_name='appt_datetime_repeat',
            new_name='repeat_appt_datetime',
        ),
        migrations.RenameField(
            model_name='historicalsubjectscreening',
            old_name='appt_datetime_repeat',
            new_name='repeat_appt_datetime',
        ),
        migrations.RenameField(
            model_name='subjectscreening',
            old_name='appt_datetime_repeat',
            new_name='repeat_appt_datetime',
        ),
    ]