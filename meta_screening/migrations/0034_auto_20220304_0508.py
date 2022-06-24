# Generated by Django 3.2.11 on 2022-03-04 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_screening", "0033_auto_20220304_0504"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="ogtt2_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                help_text="If required, must be at least 3 days after the first OGTT",
                max_length=15,
                verbose_name="In opinion of the clinician, should the OGTT be repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="ogtt2_units",
            field=models.CharField(
                blank=True,
                choices=[("mg/dL", "mg/dL"), ("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="Units (Repeat OGTT)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="ogtt_units",
            field=models.CharField(
                blank=True,
                choices=[("mg/dL", "mg/dL"), ("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="Units (OGTT)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="ogtt2_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                help_text="If required, must be at least 3 days after the first OGTT",
                max_length=15,
                verbose_name="In opinion of the clinician, should the OGTT be repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="ogtt2_units",
            field=models.CharField(
                blank=True,
                choices=[("mg/dL", "mg/dL"), ("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="Units (Repeat OGTT)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="ogtt_units",
            field=models.CharField(
                blank=True,
                choices=[("mg/dL", "mg/dL"), ("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="Units (OGTT)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="ogtt2_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                help_text="If required, must be at least 3 days after the first OGTT",
                max_length=15,
                verbose_name="In opinion of the clinician, should the OGTT be repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="ogtt2_units",
            field=models.CharField(
                blank=True,
                choices=[("mg/dL", "mg/dL"), ("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="Units (Repeat OGTT)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="ogtt_units",
            field=models.CharField(
                blank=True,
                choices=[("mg/dL", "mg/dL"), ("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="Units (OGTT)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="ogtt2_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                help_text="If required, must be at least 3 days after the first OGTT",
                max_length=15,
                verbose_name="In opinion of the clinician, should the OGTT be repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="ogtt2_units",
            field=models.CharField(
                blank=True,
                choices=[("mg/dL", "mg/dL"), ("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="Units (Repeat OGTT)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="ogtt_units",
            field=models.CharField(
                blank=True,
                choices=[("mg/dL", "mg/dL"), ("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="Units (OGTT)",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="ogtt2_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                help_text="If required, must be at least 3 days after the first OGTT",
                max_length=15,
                verbose_name="In opinion of the clinician, should the OGTT be repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="ogtt2_units",
            field=models.CharField(
                blank=True,
                choices=[("mg/dL", "mg/dL"), ("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="Units (Repeat OGTT)",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="ogtt_units",
            field=models.CharField(
                blank=True,
                choices=[("mg/dL", "mg/dL"), ("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="Units (OGTT)",
            ),
        ),
    ]
