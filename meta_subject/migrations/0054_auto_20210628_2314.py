# Generated by Django 3.2.4 on 2021-06-28 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta_subject', '0053_auto_20210628_2105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloodresultslipid',
            old_name='hdl',
            new_name='hdl_value',
        ),
        migrations.RenameField(
            model_name='bloodresultslipid',
            old_name='ldl',
            new_name='ldl_value',
        ),
        migrations.RenameField(
            model_name='bloodresultslipid',
            old_name='trig',
            new_name='trig_value',
        ),
        migrations.RenameField(
            model_name='historicalbloodresultslipid',
            old_name='hdl',
            new_name='hdl_value',
        ),
        migrations.RenameField(
            model_name='historicalbloodresultslipid',
            old_name='ldl',
            new_name='ldl_value',
        ),
        migrations.RenameField(
            model_name='historicalbloodresultslipid',
            old_name='trig',
            new_name='trig_value',
        ),
        migrations.AlterField(
            model_name='bloodresultshba1c',
            name='hba1c_quantifier',
            field=models.CharField(blank=True, choices=[('=', '='), ('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<=')], default='=', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='bloodresultshba1c',
            name='hba1c_units',
            field=models.CharField(blank=True, default='%', max_length=15, null=True, verbose_name='units'),
        ),
        migrations.AlterField(
            model_name='bloodresultshba1c',
            name='hba1c_value',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True, verbose_name='HbA1c value'),
        ),
        migrations.AlterField(
            model_name='historicalbloodresultshba1c',
            name='hba1c_quantifier',
            field=models.CharField(blank=True, choices=[('=', '='), ('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<=')], default='=', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='historicalbloodresultshba1c',
            name='hba1c_units',
            field=models.CharField(blank=True, default='%', max_length=15, null=True, verbose_name='units'),
        ),
        migrations.AlterField(
            model_name='historicalbloodresultshba1c',
            name='hba1c_value',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True, verbose_name='HbA1c value'),
        ),
    ]