# Generated by Django 3.2.11 on 2022-03-04 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0095_auto_20220128_1719"),
    ]

    operations = [
        migrations.AlterField(
            model_name="glucose",
            name="ifg_datetime",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="<u>Time</u> FBG level measured"
            ),
        ),
        migrations.AlterField(
            model_name="glucose",
            name="ifg_quantifier",
            field=models.CharField(
                choices=[
                    ("=", "="),
                    (">", ">"),
                    (">=", ">="),
                    ("<", "<"),
                    ("<=", "<="),
                ],
                default="=",
                max_length=10,
                verbose_name="FBG quantifier",
            ),
        ),
        migrations.AlterField(
            model_name="glucose",
            name="ifg_units",
            field=models.CharField(
                choices=[
                    ("mg/dL", "mg/dL"),
                    ("mmol/L", "mmol/L (millimoles/L)"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                verbose_name="FBG units",
            ),
        ),
        migrations.AlterField(
            model_name="glucose",
            name="ifg_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="A `HIGH` reading may be entered as 9999.99",
                max_digits=8,
                null=True,
                verbose_name="FBG level",
            ),
        ),
        migrations.AlterField(
            model_name="historicalglucose",
            name="ifg_datetime",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="<u>Time</u> FBG level measured"
            ),
        ),
        migrations.AlterField(
            model_name="historicalglucose",
            name="ifg_quantifier",
            field=models.CharField(
                choices=[
                    ("=", "="),
                    (">", ">"),
                    (">=", ">="),
                    ("<", "<"),
                    ("<=", "<="),
                ],
                default="=",
                max_length=10,
                verbose_name="FBG quantifier",
            ),
        ),
        migrations.AlterField(
            model_name="historicalglucose",
            name="ifg_units",
            field=models.CharField(
                choices=[
                    ("mg/dL", "mg/dL"),
                    ("mmol/L", "mmol/L (millimoles/L)"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                verbose_name="FBG units",
            ),
        ),
        migrations.AlterField(
            model_name="historicalglucose",
            name="ifg_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="A `HIGH` reading may be entered as 9999.99",
                max_digits=8,
                null=True,
                verbose_name="FBG level",
            ),
        ),
    ]
