# Generated by Django 2.2.11 on 2020-03-25 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_consent", "0002_auto_20191024_1000"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="identity_type",
            field=models.CharField(
                choices=[
                    ("country_id", "Country ID number"),
                    ("drivers", "Driver's license"),
                    ("passport", "Passport"),
                    ("hospital_no", "Hospital number"),
                    ("country_id_rcpt", "Country ID receipt"),
                    ("mobile_no", "Mobile number"),
                    ("OTHER", "Other"),
                ],
                max_length=25,
                verbose_name="What type of identity number is this?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="identity_type",
            field=models.CharField(
                choices=[
                    ("country_id", "Country ID number"),
                    ("drivers", "Driver's license"),
                    ("passport", "Passport"),
                    ("hospital_no", "Hospital number"),
                    ("country_id_rcpt", "Country ID receipt"),
                    ("mobile_no", "Mobile number"),
                    ("OTHER", "Other"),
                ],
                max_length=25,
                verbose_name="What type of identity number is this?",
            ),
        ),
    ]
