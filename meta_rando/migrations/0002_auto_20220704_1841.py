# Generated by Django 3.2.13 on 2022-07-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta_rando', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalrandomizationlist',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Randomization List (Phase Three)', 'verbose_name_plural': 'historical Randomization List (Phase Three)'},
        ),
        migrations.AlterField(
            model_name='historicalrandomizationlist',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]