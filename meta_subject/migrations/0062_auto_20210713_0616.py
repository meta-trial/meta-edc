# Generated by Django 3.2.4 on 2021-07-13 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta_subject', '0061_auto_20210710_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodresultsrft',
            name='creatinine_units',
            field=models.CharField(blank=True, choices=[('mg/dL', 'mg/dL'), ('umol/L', 'μmol/L (micromoles/L)')], max_length=25, null=True, verbose_name='units'),
        ),
        migrations.AlterField(
            model_name='historicalbloodresultsrft',
            name='creatinine_units',
            field=models.CharField(blank=True, choices=[('mg/dL', 'mg/dL'), ('umol/L', 'μmol/L (micromoles/L)')], max_length=25, null=True, verbose_name='units'),
        ),
    ]