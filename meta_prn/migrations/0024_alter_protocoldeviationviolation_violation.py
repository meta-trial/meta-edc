# Generated by Django 4.0.5 on 2022-06-24 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edc_protocol_violation', '0004_alter_protocoldeviationviolation_violation'),
        ('meta_prn', '0023_auto_20220415_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocoldeviationviolation',
            name='violation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='edc_protocol_violation.protocolviolations', verbose_name='Type of violation'),
        ),
    ]