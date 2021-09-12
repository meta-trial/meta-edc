# Generated by Django 3.2.6 on 2021-09-11 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta_prn', '0012_auto_20210911_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endofstudy',
            name='tracking_identifier',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='historicalendofstudy',
            name='tracking_identifier',
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='historicallosstofollowup',
            name='tracking_identifier',
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='historicalprotocoldeviationviolation',
            name='safety_impact',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', max_length=25, verbose_name='Could this occurrence have an impact on safety of the participant?'),
        ),
        migrations.AlterField(
            model_name='historicalprotocoldeviationviolation',
            name='study_outcomes_impact',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', max_length=25, verbose_name='Could this occurrence have an impact on study outcomes?'),
        ),
        migrations.AlterField(
            model_name='historicalprotocoldeviationviolation',
            name='tracking_identifier',
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='losstofollowup',
            name='tracking_identifier',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='protocoldeviationviolation',
            name='safety_impact',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', max_length=25, verbose_name='Could this occurrence have an impact on safety of the participant?'),
        ),
        migrations.AlterField(
            model_name='protocoldeviationviolation',
            name='study_outcomes_impact',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', max_length=25, verbose_name='Could this occurrence have an impact on study outcomes?'),
        ),
        migrations.AlterField(
            model_name='protocoldeviationviolation',
            name='tracking_identifier',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
