# Generated by Django 5.1 on 2024-09-09 20:38

import django_db_views.migration_functions
import django_db_views.operations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0047_impsubstitutions"),
    ]

    operations = [
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "select *, uuid() as id, now() as `created`, 'meta_reports.imp_subjectitutions_view' as `report_model` from (SELECT s.subject_identifier, s.sid, s.dispensed_sid, arm_match, r.allocated_datetime, s.site_id, s.user_created, s.user_modified, s.modified, s.id AS original_id FROM meta_pharmacy_substitutions AS s LEFT JOIN meta_rando_randomizationlist AS r ON r.subject_identifier = s.subject_identifier ORDER BY s.subject_identifier) as A ORDER BY subject_identifier, site_id",
                "imp_subjectitutions_view",
                engine="django.db.backends.mysql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "", "imp_subjectitutions_view", engine="django.db.backends.mysql"
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "select *, get_random_uuid() as id, now() as created, 'meta_reports.imp_subjectitutions_view' as report_model from (SELECT s.subject_identifier, s.sid, s.dispensed_sid, arm_match, r.allocated_datetime, s.site_id, s.user_created, s.user_modified, s.modified, s.id AS original_id FROM meta_pharmacy_substitutions AS s LEFT JOIN meta_rando_randomizationlist AS r ON r.subject_identifier = s.subject_identifier ORDER BY s.subject_identifier NULLS FIRST) as A ORDER BY subject_identifier, site_id",
                "imp_subjectitutions_view",
                engine="django.db.backends.postgresql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "", "imp_subjectitutions_view", engine="django.db.backends.postgresql"
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "select *, uuid() as id, datetime() as created, 'meta_reports.imp_subjectitutions_view' as report_model from (SELECT s.subject_identifier, s.sid, s.dispensed_sid, arm_match, r.allocated_datetime, s.site_id, s.user_created, s.user_modified, s.modified, s.id AS original_id FROM meta_pharmacy_substitutions AS s LEFT JOIN meta_rando_randomizationlist AS r ON r.subject_identifier = s.subject_identifier ORDER BY s.subject_identifier) as A ORDER BY subject_identifier, site_id",
                "imp_subjectitutions_view",
                engine="django.db.backends.sqlite3",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "", "imp_subjectitutions_view", engine="django.db.backends.sqlite3"
            ),
            atomic=False,
        ),
    ]