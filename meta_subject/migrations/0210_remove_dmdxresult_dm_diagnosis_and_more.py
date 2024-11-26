# Generated by Django 5.0.8 on 2024-08-21 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0209_remove_historicaldmdxresult_dm_diagnosis_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dmdxresult",
            name="dm_diagnosis",
        ),
        migrations.RemoveField(
            model_name="dmdxresult",
            name="site",
        ),
        migrations.RemoveField(
            model_name="historicaldmdxresult",
            name="dm_diagnosis",
        ),
        migrations.RemoveField(
            model_name="historicaldmdxresult",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicaldmdxresult",
            name="site",
        ),
        migrations.AlterModelOptions(
            name="dmendpoint",
            options={
                "default_manager_name": "objects",
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "verbose_name": "Diabetes endpoint",
                "verbose_name_plural": "Diabetes endpoint",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaldmendpoint",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Diabetes endpoint",
                "verbose_name_plural": "historical Diabetes endpoint",
            },
        ),
        migrations.RenameIndex(
            model_name="dmendpoint",
            new_name="meta_subjec_subject_03eaba_idx",
            old_name="meta_subjec_subject_40b1c1_idx",
        ),
        migrations.RenameIndex(
            model_name="dmendpoint",
            new_name="meta_subjec_subject_605359_idx",
            old_name="meta_subjec_subject_2059c2_idx",
        ),
        migrations.AlterField(
            model_name="dmendpoint",
            name="dx_date",
            field=models.DateField(verbose_name="Date endpoint reached"),
        ),
        migrations.AlterField(
            model_name="dmendpoint",
            name="dx_initiated_by",
            field=models.CharField(
                default="QUESTION_RETIRED",
                max_length=25,
                verbose_name="What initiated the diagnosis",
            ),
        ),
        migrations.AlterField(
            model_name="dmendpoint",
            name="dx_tmg",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("QUESTION_RETIRED", "Question retired"),
                ],
                default="QUESTION_RETIRED",
                max_length=25,
                verbose_name="Was this case discussed with the TMG?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldmendpoint",
            name="dx_date",
            field=models.DateField(verbose_name="Date endpoint reached"),
        ),
        migrations.AlterField(
            model_name="historicaldmendpoint",
            name="dx_initiated_by",
            field=models.CharField(
                default="QUESTION_RETIRED",
                max_length=25,
                verbose_name="What initiated the diagnosis",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldmendpoint",
            name="dx_tmg",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("QUESTION_RETIRED", "Question retired"),
                ],
                default="QUESTION_RETIRED",
                max_length=25,
                verbose_name="Was this case discussed with the TMG?",
            ),
        ),
        migrations.DeleteModel(
            name="DmDxResult",
        ),
        migrations.DeleteModel(
            name="HistoricalDmDxResult",
        ),
    ]