# Generated by Django 2.2.6 on 2019-10-24 07:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("meta_subject", "0004_auto_20191022_0134")]

    operations = [
        migrations.AlterField(
            model_name="bloodresultsfbc",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultsglu",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultshba1c",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultslft",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultsrft",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="complications",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="followupvitals",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomics",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="malariarapidtest",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="medicationadherence",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="subjectrequisition",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="urinedipsticktest",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        ),
    ]
