# Generated by Django 5.0.8 on 2024-08-23 13:42

import django_db_views.migration_functions
import django_db_views.operations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0033_auto_20240823_0012"),
    ]

    operations = [
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\n    select *, uuid() as id, now() as created,\n    'meta_reports.missing_screening_ogtt_view' as report_model\n      from (\n        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,\n        converted_fbg_value as fbg_value,  converted_ogtt_value as ogtt_value, repeat_glucose_performed as repeated,\n        p3_ltfu, fbg2_value, ogtt2_value, fbg2_datetime, ogtt2_datetime, consented,\n        screening_identifier as subject_identifier, id as original_id\n        from meta_screening_subjectscreening\n        where converted_fbg_value is not null and converted_ogtt_value is null and unsuitable_agreed != \"Yes\"\n    ) as A\n    order by screening_identifier",
                "missing_screening_ogtt_view",
                engine="django.db.backends.mysql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "# noqa\n    select *, uuid() as id, now() as created,\n    'meta_reports.missing_screening_ogtt_view' as report_model\n      from (\n        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,\n        converted_fbg_value as fbg_value,  converted_ogtt_value as ogtt_value, repeat_glucose_performed as repeated,\n        p3_ltfu, fbg2_value, ogtt2_value, fbg2_datetime, ogtt2_datetime, consented, \"\" as subject_identifier,\n        id as original_id\n        from meta_screening_subjectscreening\n        where converted_fbg_value is not null and converted_ogtt_value is null and unsuitable_agreed != \"Yes\"\n    ) as A\n    order by screening_identifier",
                "missing_screening_ogtt_view",
                engine="django.db.backends.mysql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\n    select *, get_random_uuid() as id, now() as created,\n    'meta_reports.missing_screening_ogtt_view' as report_model\n      from (\n        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,\n        converted_fbg_value as fbg_value,  converted_ogtt_value as ogtt_value, repeat_glucose_performed as repeated,\n        p3_ltfu, fbg2_value, ogtt2_value, fbg2_datetime, ogtt2_datetime, consented,\n        screening_identifier as subject_identifier, id as original_id\n        from meta_screening_subjectscreening\n        where converted_fbg_value is not null and converted_ogtt_value is null and unsuitable_agreed != \"Yes\"\n    ) as A\n    order by screening_identifier",
                "missing_screening_ogtt_view",
                engine="django.db.backends.postgresql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "# noqa\n    select *, get_random_uuid() as id, now() as created,\n    'meta_reports.missing_screening_ogtt_view' as report_model\n      from (\n        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,\n        converted_fbg_value as fbg_value,  converted_ogtt_value as ogtt_value, repeat_glucose_performed as repeated,\n        p3_ltfu, fbg2_value, ogtt2_value, fbg2_datetime, ogtt2_datetime, consented, \"\" as subject_identifier,\n        id as original_id\n        from meta_screening_subjectscreening\n        where converted_fbg_value is not null and converted_ogtt_value is null and unsuitable_agreed != \"Yes\"\n    ) as A\n    order by screening_identifier",
                "missing_screening_ogtt_view",
                engine="django.db.backends.postgresql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\nSELECT *, lower(\n    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n    substr(hex( randomblob(2)), 2) || '-' ||\n    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n    substr(hex(randomblob(2)), 2) || '-' ||\n    hex(randomblob(6))\n  ) as id, datetime() as `created`,\n    'meta_reports.missing_screening_ogtt_view' as report_model\n      from (\n        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,\n        converted_fbg_value as fbg_value,  converted_ogtt_value as ogtt_value, fbg2_value, ogtt2_value,\n        repeat_glucose_performed as repeated, p3_ltfu, fbg2_datetime, ogtt2_datetime, consented,\n        screening_identifier as subject_identifier, id as original_id\n        from meta_screening_subjectscreening\n        where converted_fbg_value is not null and converted_ogtt_value is null and unsuitable_agreed != \"Yes\"\n    ) as A\n    order by screening_identifier",
                "missing_screening_ogtt_view",
                engine="django.db.backends.sqlite3",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "# noqa\nSELECT *, lower(\n    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n    substr(hex( randomblob(2)), 2) || '-' ||\n    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n    substr(hex(randomblob(2)), 2) || '-' ||\n    hex(randomblob(6))\n  ) as id, datetime() as `created`,\n    'meta_reports.missing_screening_ogtt_view' as report_model\n      from (\n        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,\n        converted_fbg_value as fbg_value,  converted_ogtt_value as ogtt_value, fbg2_value, ogtt2_value,\n        repeat_glucose_performed as repeated, p3_ltfu, fbg2_datetime, ogtt2_datetime, consented, \"\" as subject_identifier,\n        id as original_id\n        from meta_screening_subjectscreening\n        where converted_fbg_value is not null and converted_ogtt_value is null and unsuitable_agreed != \"Yes\"\n    ) as A\n    order by screening_identifier",
                "missing_screening_ogtt_view",
                engine="django.db.backends.sqlite3",
            ),
            atomic=False,
        ),
    ]
