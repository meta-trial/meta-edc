# Generated by Django 5.0.7 on 2024-08-12 22:56

import django_db_views.migration_functions
import django_db_views.operations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0010_alter_patienthistorymissingbaselinecd4_options_and_more"),
    ]

    operations = [
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "select *, uuid() as id, now() as created, \n    'meta_reports.patienthistorymissingbaselinecd4' as report_model \n      from (\n        select subject_identifier, v.visit_code, v.visit_code_sequence,cd4,\n          cd4_date, crf.site_id, crf.user_created, crf.user_modified,\n          crf.modified\n        from meta_subject_patienthistory as crf\n        left join meta_subject_subjectvisit as v on crf.subject_visit_id=v.id\n        where cd4 is null or cd4_date is null\n    ) as A\n    order by subject_identifier",
                "patient_history_missing_baseline_cd4_view",
                engine="django.db.backends.mysql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "",
                "patient_history_missing_baseline_cd4_view",
                engine="django.db.backends.mysql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "select *, get_random_uuid() as id, now() as created, \n    'meta_reports.patienthistorymissingbaselinecd4' as report_model \n      from (\n        select subject_identifier, v.visit_code, v.visit_code_sequence,cd4,\n          cd4_date, crf.site_id, crf.user_created, crf.user_modified,\n          crf.modified\n        from meta_subject_patienthistory as crf\n        left join meta_subject_subjectvisit as v on crf.subject_visit_id=v.id\n        where cd4 is null or cd4_date is null\n    ) as A\n    order by subject_identifier",
                "patient_history_missing_baseline_cd4_view",
                engine="django.db.backends.postgresql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "",
                "patient_history_missing_baseline_cd4_view",
                engine="django.db.backends.postgresql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "SELECT *, lower(\n    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n    substr(hex( randomblob(2)), 2) || '-' ||\n    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n    substr(hex(randomblob(2)), 2) || '-' ||\n    hex(randomblob(6))\n  ) as id, datetime() as `created`, 'meta_reports.patienthistorymissingbaselinecd4' as report_model \n      from (\n        select subject_identifier, v.visit_code, v.visit_code_sequence,cd4,\n          cd4_date, crf.site_id, crf.user_created, crf.user_modified,\n          crf.modified\n        from meta_subject_patienthistory as crf\n        left join meta_subject_subjectvisit as v on crf.subject_visit_id=v.id\n        where cd4 is null or cd4_date is null\n    ) as A\n    order by subject_identifier",
                "patient_history_missing_baseline_cd4_view",
                engine="django.db.backends.sqlite3",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "",
                "patient_history_missing_baseline_cd4_view",
                engine="django.db.backends.sqlite3",
            ),
            atomic=False,
        ),
    ]
