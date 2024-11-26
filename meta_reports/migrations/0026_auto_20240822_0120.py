# Generated by Django 5.0.8 on 2024-08-21 22:20

import django_db_views.migration_functions
import django_db_views.operations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0025_auto_20240822_0115"),
    ]

    operations = [
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\nselect *, uuid() as id, now() as created, 'meta_reports.glucose_summary_view' as report_model\nfrom (\n    select subject_identifier, fbg_value, fbg_datetime, null as 'ogtt_value', null as 'ogtt_datetime', fbg.site_id  \n    from meta_subject_glucosefbg as fbg \n    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id\n    UNION\n    select subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime, fbg.site_id\n    from meta_subject_glucose as fbg \n    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id) as A\norder by subject_identifier, fbg_datetime",
                "glucose_summary_view",
                engine="django.db.backends.mysql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "# noqa\nselect subject_identifier, fbg_value, fbg_datetime, null as 'ogtt_value', null as 'ogtt_datetime',\nfbg.site_id, 'glucose_summary_view' as report_model \nfrom meta_subject_glucosefbg as fbg \nleft join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id\nUNION\nselect subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime,\nfbg.site_id, 'glucose_summary_view' as report_model\nfrom meta_subject_glucose as fbg \nleft join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id\norder by subject_identifier, fbg_datetime",
                "glucose_summary_view",
                engine="django.db.backends.mysql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\nselect *, get_random_uuid() as id, now() as created, 'meta_reports.glucose_summary_view' as report_model\nfrom (\n    select subject_identifier, fbg_value, fbg_datetime, null as ogtt_value, null as ogtt_datetime, fbg.site_id\n    from meta_subject_glucosefbg as fbg \n    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id\n    UNION\n    select subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime, fbg.site_id\n    from meta_subject_glucose as fbg \n    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id) as A\norder by subject_identifier, fbg_datetime",
                "glucose_summary_view",
                engine="django.db.backends.postgresql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "# noqa\nselect subject_identifier, fbg_value, fbg_datetime, null as ogtt_value, null as ogtt_datetime,\nfbg.site_id, 'glucose_summary_view' as report_model\nfrom meta_subject_glucosefbg as fbg \nleft join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id\nUNION\nselect subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime,\nfbg.site_id, 'glucose_summary_view' as report_model\nfrom meta_subject_glucose as fbg \nleft join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id\norder by subject_identifier, fbg_datetime",
                "glucose_summary_view",
                engine="django.db.backends.postgresql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\nSELECT *, lower(\n    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n    substr(hex( randomblob(2)), 2) || '-' ||\n    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n    substr(hex(randomblob(2)), 2) || '-' ||\n    hex(randomblob(6))\n  ) as id, datetime() as `created`, 'meta_reports.glucose_summary_view' as report_model\nfrom (\n    select subject_identifier, fbg_value, fbg_datetime, null as ogtt_value, null as ogtt_datetime,\n    fbg.site_id, 'glucose_summary_view' as report_model\n    from meta_subject_glucosefbg as fbg \n    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id\n    UNION\n    select subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime,\n    fbg.site_id, 'glucose_summary_view' as report_model\n    from meta_subject_glucose as fbg \n    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id) as A\norder by subject_identifier, fbg_datetime",
                "glucose_summary_view",
                engine="django.db.backends.sqlite3",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "# noqa\nselect subject_identifier, fbg_value, fbg_datetime, null as ogtt_value, null as ogtt_datetime,\nfbg.site_id, 'glucose_summary_view' as report_model\nfrom meta_subject_glucosefbg as fbg \nleft join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id\nUNION\nselect subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime,\nfbg.site_id, 'glucose_summary_view' as report_model\nfrom meta_subject_glucose as fbg \nleft join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id\norder by subject_identifier, fbg_datetime",
                "glucose_summary_view",
                engine="django.db.backends.sqlite3",
            ),
            atomic=False,
        ),
    ]