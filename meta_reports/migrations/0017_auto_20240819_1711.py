# Generated by Django 5.1 on 2024-08-19 14:11

import django_db_views.migration_functions
import django_db_views.operations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0016_missingscreeningogtt"),
        ("meta_screening", "0067_alter_historicalscreeningpartone_report_datetime_and_more"),
    ]

    operations = [
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "select *, uuid() as id, now() as created,\n    'meta_reports.missing_screening_ogtt_view' as report_model\n      from (\n        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,\n        fbg_value,  ogtt_value, fbg2_value, ogtt2_value, fbg2_datetime, ogtt2_datetime, consented \n        from meta_screening_subjectscreening \n        where fbg_value is not null and ogtt_value is null\n    ) as A\n    order by screening_identifier",
                "missing_screening_ogtt_view",
                engine="django.db.backends.mysql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "", "missing_screening_ogtt_view", engine="django.db.backends.mysql"
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "select *, get_random_uuid() as id, now() as created,\n    'meta_reports.missing_screening_ogtt_view' as report_model\n      from (\n        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,\n        fbg_value,  ogtt_value, fbg2_value, ogtt2_value, fbg2_datetime, ogtt2_datetime, consented \n        from meta_screening_subjectscreening \n        where fbg_value is not null and ogtt_value is null\n    ) as A\n    order by screening_identifier",
                "missing_screening_ogtt_view",
                engine="django.db.backends.postgresql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "", "missing_screening_ogtt_view", engine="django.db.backends.postgresql"
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "SELECT *, lower(\n    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n    substr(hex( randomblob(2)), 2) || '-' ||\n    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n    substr(hex(randomblob(2)), 2) || '-' ||\n    hex(randomblob(6))\n  ) as id, datetime() as `created`,\n    'meta_reports.missing_screening_ogtt_view' as report_model\n      from (\n        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,\n        fbg_value,  ogtt_value, fbg2_value, ogtt2_value, fbg2_datetime, ogtt2_datetime, consented \n        from meta_screening_subjectscreening \n        where fbg_value is not null and ogtt_value is null\n    ) as A\n    order by screening_identifier",
                "missing_screening_ogtt_view",
                engine="django.db.backends.sqlite3",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "", "missing_screening_ogtt_view", engine="django.db.backends.sqlite3"
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\n    select *, uuid() as id, now() as created, 'meta_reports.unattendedthreeinrow' as `report_model` from (\n        select subject_identifier, site_id, appt_datetime, `first_value`, `second_value`, `third_value`,\n            datediff(third_date, first_date) as `interval_days`,\n            datediff(now(), first_date) as `from_now_days`\n        from (\n            select subject_identifier, site_id, appt_datetime,\n            FIRST_VALUE(visit_code) OVER w as `first_value`,\n            NTH_VALUE(visit_code, 2) OVER w as `second_value`,\n            NTH_VALUE(visit_code, 3) OVER w as `third_value`,\n            FIRST_VALUE(appt_datetime) OVER w as `first_date`,\n            NTH_VALUE(appt_datetime, 3) OVER w as `third_date`\n            from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n            and appt_datetime <= now()\n            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n        ) as A\n    where `second_value` is not null and `third_value` is not null\n    ) as B\n    order by site_id, from_now_days desc",
                "unattended_three_in_row_view",
                engine="django.db.backends.mysql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "select *, uuid() as id, now() as created, 'meta_reports.unattendedthreeinrow' as `report_model` from (\n        select subject_identifier, site_id, appt_datetime, `first_value`, `second_value`, `third_value`,\n            datediff(third_date, first_date) as `interval_days`,\n            datediff(now(), first_date) as `from_now_days`\n        from (\n            select subject_identifier, site_id, appt_datetime,\n            FIRST_VALUE(visit_code) OVER w as `first_value`,\n            NTH_VALUE(visit_code, 2) OVER w as `second_value`,\n            NTH_VALUE(visit_code, 3) OVER w as `third_value`,\n            FIRST_VALUE(appt_datetime) OVER w as `first_date`,\n            NTH_VALUE(appt_datetime, 3) OVER w as `third_date`\n            from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n            and appt_datetime <= now()\n            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n        ) as A\n    where `second_value` is not null and `third_value` is not null\n    ) as B\n    order by site_id, from_now_days desc",
                "unattended_three_in_row_view",
                engine="django.db.backends.mysql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\n    select *, gen_random_uuid() as id, now() as created,\n    'meta_reports.unattendedthreeinrow' as report_model\n    from (\n    select subject_identifier, site_id, appt_datetime, first_value, second_value, third_value,\n    EXTRACT(DAY FROM third_date - first_date) as interval_days,\n    EXTRACT(DAY FROM now() - first_date) as from_now_days\n    from (\n    select subject_identifier,site_id,appt_datetime,\n    FIRST_VALUE(visit_code) OVER w as first_value,\n    NTH_VALUE(visit_code, 2) OVER w as second_value,\n    NTH_VALUE(visit_code, 3) OVER w as third_value,\n    FIRST_VALUE(appt_datetime) OVER w as first_date,\n    NTH_VALUE(appt_datetime, 3) OVER w as third_date\n    from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n    and appt_datetime <= now()\n    WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n    ) as A\n    where second_value is not null and third_value is not null\n    ) as B\n    order by site_id, from_now_days desc",
                "unattended_three_in_row_view",
                engine="django.db.backends.postgresql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "select *, gen_random_uuid() as id, now() as created, \n    'meta_reports.unattendedthreeinrow' as report_model \n    from (\n    select subject_identifier, site_id, appt_datetime, first_value, second_value, third_value,\n    EXTRACT(DAY FROM third_date - first_date) as interval_days,\n    EXTRACT(DAY FROM now() - first_date) as from_now_days \n    from (\n    select subject_identifier,site_id,appt_datetime,\n    FIRST_VALUE(visit_code) OVER w as first_value,\n    NTH_VALUE(visit_code, 2) OVER w as second_value,\n    NTH_VALUE(visit_code, 3) OVER w as third_value,\n    FIRST_VALUE(appt_datetime) OVER w as first_date,\n    NTH_VALUE(appt_datetime, 3) OVER w as third_date\n    from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n    and appt_datetime <= now()\n    WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n    ) as A\n    where second_value is not null and third_value is not null\n    ) as B\n    order by site_id, from_now_days desc",
                "unattended_three_in_row_view",
                engine="django.db.backends.postgresql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\nSELECT *, lower(\n    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n    substr(hex( randomblob(2)), 2) || '-' ||\n    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n    substr(hex(randomblob(2)), 2) || '-' ||\n    hex(randomblob(6))\n  ) as id, datetime() as created,'meta_reports.unattendedthreeinrow' as report_model from (\n        select subject_identifier, site_id, appt_datetime, first_value, second_value, third_value,\n            CAST(JulianDay(third_date) - JulianDay(first_date) AS INTEGER) as interval_days,\n            CAST(JulianDay(datetime()) - JulianDay(first_date) AS INTEGER) as from_now_days\n        from (\n            select subject_identifier, site_id, appt_datetime,\n            FIRST_VALUE(visit_code) OVER w as first_value,\n            NTH_VALUE(visit_code, 2) OVER w as second_value,\n            NTH_VALUE(visit_code, 3) OVER w as third_value,\n            FIRST_VALUE(appt_datetime) OVER w as first_date,\n            NTH_VALUE(appt_datetime, 3) OVER w as third_date\n            from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n            and appt_datetime <= datetime()\n            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n        ) as A\n    where second_value is not null and third_value is not null\n    ) as B\n    order by site_id, from_now_days desc",
                "unattended_three_in_row_view",
                engine="django.db.backends.sqlite3",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "SELECT *, lower(\n    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n    substr(hex( randomblob(2)), 2) || '-' ||\n    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n    substr(hex(randomblob(2)), 2) || '-' ||\n    hex(randomblob(6))\n  ) as id, datetime() as created,'meta_reports.unattendedthreeinrow' as report_model from (\n        select subject_identifier, site_id, appt_datetime, first_value, second_value, third_value,\n            CAST(JulianDay(third_date) - JulianDay(first_date) AS Integer) as interval_days,\n            CAST(JulianDay(datetime()) - JulianDay(first_date) AS Integer) as from_now_days\n        from (\n            select subject_identifier, site_id, appt_datetime,\n            FIRST_VALUE(visit_code) OVER w as first_value,\n            NTH_VALUE(visit_code, 2) OVER w as second_value,\n            NTH_VALUE(visit_code, 3) OVER w as third_value,\n            FIRST_VALUE(appt_datetime) OVER w as first_date,\n            NTH_VALUE(appt_datetime, 3) OVER w as third_date\n            from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n            and appt_datetime <= datetime()\n            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n        ) as A\n    where second_value is not null and third_value is not null\n    ) as B\n    order by site_id, from_now_days desc",
                "unattended_three_in_row_view",
                engine="django.db.backends.sqlite3",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\n    with appointments as (\n        select subject_identifier, site_id, visit_code, visit_code_sequence, appt_datetime,\n        case when appt_timing='missed' then 'New' else appt_status end as `appt_status`,\n        case when appt_timing='missed' then 1 else 0 end as `missed`\n        from edc_appointment_appointment\n        where visit_code_sequence=0 and appt_datetime<=now()\n        order by subject_identifier, appt_datetime\n        )\n    select *, uuid() as `id`, now() as `created`, 'meta_reports.unattendedthreeinrow2' as `report_model` from (\n        select  distinct subject_identifier, site_id,  `first_value`, `second_value`, `third_value`,\n            datediff(third_date, first_date) as `interval_days`,\n            datediff(now(), first_date) as `from_now_days`,\n            `first_status`, `second_status`, `third_status`, sum(missed) as `missed_count`\n        from (\n            select subject_identifier,site_id,appt_datetime, missed,\n            FIRST_VALUE(appt_status) OVER w as `third_status`,\n            NTH_VALUE(appt_status, 2) OVER w as `second_status`,\n            NTH_VALUE(appt_status, 3) OVER w as `first_status`,\n            FIRST_VALUE(visit_code) OVER w as `third_value`,\n            NTH_VALUE(visit_code, 2) OVER w as `second_value`,\n            NTH_VALUE(visit_code, 3) OVER w as `first_value`,\n            FIRST_VALUE(appt_datetime) OVER w as `third_date`,\n            NTH_VALUE(appt_datetime, 2) OVER w as `second_date`,\n            NTH_VALUE(appt_datetime, 3) OVER w as `first_date`\n            from appointments\n            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime desc ROWS UNBOUNDED PRECEDING)\n        ) as A\n        where `second_value` is not null and `third_value` is not null\n          and `first_status`='New'\n          and `second_status`='New'\n          and `third_status`='New'\n        group by subject_identifier, site_id,  `first_value`, `second_value`, `third_value`,\n                 datediff(`third_date`, `first_date`),\n                 datediff(now(), `first_date`),\n                 `first_status`, `second_status`, `third_status`\n        order by subject_identifier, site_id\n    ) as B",
                "unattended_three_in_row2_view",
                engine="django.db.backends.mysql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "with appointments as (\n        select subject_identifier, site_id, visit_code, visit_code_sequence, appt_datetime,\n        case when appt_timing='missed' then 'New' else appt_status end as `appt_status`,\n        case when appt_timing='missed' then 1 else 0 end as `missed`\n        from edc_appointment_appointment\n        where visit_code_sequence=0 and appt_datetime<=now()\n        order by subject_identifier, appt_datetime\n        )\n    select *, uuid() as `id`, now() as `created`, 'meta_reports.unattendedthreeinrow2' as `report_model` from (\n        select  distinct subject_identifier, site_id,  `first_value`, `second_value`, `third_value`,\n            datediff(third_date, first_date) as `interval_days`,\n            datediff(now(), first_date) as `from_now_days`,\n            `first_status`, `second_status`, `third_status`, sum(missed) as `missed_count`\n        from (\n            select subject_identifier,site_id,appt_datetime, missed,\n            FIRST_VALUE(appt_status) OVER w as `third_status`,\n            NTH_VALUE(appt_status, 2) OVER w as `second_status`,\n            NTH_VALUE(appt_status, 3) OVER w as `first_status`,\n            FIRST_VALUE(visit_code) OVER w as `third_value`,\n            NTH_VALUE(visit_code, 2) OVER w as `second_value`,\n            NTH_VALUE(visit_code, 3) OVER w as `first_value`,\n            FIRST_VALUE(appt_datetime) OVER w as `third_date`,\n            NTH_VALUE(appt_datetime, 2) OVER w as `second_date`,\n            NTH_VALUE(appt_datetime, 3) OVER w as `first_date`\n            from appointments\n            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime desc ROWS UNBOUNDED PRECEDING)\n        ) as A\n        where `second_value` is not null and `third_value` is not null\n          and `first_status`='New'\n          and `second_status`='New'\n          and `third_status`='New'\n        group by subject_identifier, site_id,  `first_value`, `second_value`, `third_value`,\n                 datediff(`third_date`, `first_date`),\n                 datediff(now(), `first_date`),\n                 `first_status`, `second_status`, `third_status`\n        order by subject_identifier, site_id\n    ) as B",
                "unattended_three_in_row2_view",
                engine="django.db.backends.mysql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\n    with appointments as (\n        select subject_identifier, site_id, visit_code, visit_code_sequence, appt_datetime,\n        case when appt_timing='missed' then 'New' else appt_status end as appt_status,\n        case when appt_timing='missed' then 1 else 0 end as missed\n        from edc_appointment_appointment\n        where visit_code_sequence=0 and appt_datetime<=now()\n        order by subject_identifier, appt_datetime\n        )\n    select *, gen_random_uuid() as id, now() as created, 'meta_reports.unattendedthreeinrow2' as report_model\n    from (\n        select  distinct subject_identifier, site_id,  first_value, second_value, third_value,\n            EXTRACT(DAY FROM third_date - first_date) as interval_days,\n            EXTRACT(DAY FROM now() - first_date) as from_now_days,\n            first_status, second_status, third_status, sum(missed) as missed_count\n        from (\n            select subject_identifier,site_id,appt_datetime, missed,\n            FIRST_VALUE(appt_status) OVER w as third_status,\n            NTH_VALUE(appt_status, 2) OVER w as second_status,\n            NTH_VALUE(appt_status, 3) OVER w as first_status,\n            FIRST_VALUE(visit_code) OVER w as third_value,\n            NTH_VALUE(visit_code, 2) OVER w as second_value,\n            NTH_VALUE(visit_code, 3) OVER w as first_value,\n            FIRST_VALUE(appt_datetime) OVER w as third_date,\n            NTH_VALUE(appt_datetime, 2) OVER w as second_date,\n            NTH_VALUE(appt_datetime, 3) OVER w as first_date\n            from appointments\n            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime desc ROWS UNBOUNDED PRECEDING)\n        ) as A\n        where second_value is not null and third_value is not null\n          and first_status='New'\n          and second_status='New'\n          and third_status='New'\n        group by subject_identifier, site_id,  first_value, second_value, third_value,\n                 EXTRACT(DAY FROM third_date - first_date),\n                 EXTRACT(DAY FROM now() - first_date),\n                 first_status, second_status, third_status\n        order by subject_identifier, site_id\n    ) as B",
                "unattended_three_in_row2_view",
                engine="django.db.backends.postgresql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "with appointments as (\n        select subject_identifier, site_id, visit_code, visit_code_sequence, appt_datetime,\n        case when appt_timing='missed' then 'New' else appt_status end as appt_status,\n        case when appt_timing='missed' then 1 else 0 end as missed\n        from edc_appointment_appointment\n        where visit_code_sequence=0 and appt_datetime<=now()\n        order by subject_identifier, appt_datetime\n        )\n    select *, gen_random_uuid() as id, now() as created, 'meta_reports.unattendedthreeinrow2' as report_model \n    from (\n        select  distinct subject_identifier, site_id,  first_value, second_value, third_value,\n            EXTRACT(DAY FROM third_date - first_date) as interval_days,\n            EXTRACT(DAY FROM now() - first_date) as from_now_days,\n            first_status, second_status, third_status, sum(missed) as missed_count\n        from (\n            select subject_identifier,site_id,appt_datetime, missed,\n            FIRST_VALUE(appt_status) OVER w as third_status,\n            NTH_VALUE(appt_status, 2) OVER w as second_status,\n            NTH_VALUE(appt_status, 3) OVER w as first_status,\n            FIRST_VALUE(visit_code) OVER w as third_value,\n            NTH_VALUE(visit_code, 2) OVER w as second_value,\n            NTH_VALUE(visit_code, 3) OVER w as first_value,\n            FIRST_VALUE(appt_datetime) OVER w as third_date,\n            NTH_VALUE(appt_datetime, 2) OVER w as second_date,\n            NTH_VALUE(appt_datetime, 3) OVER w as first_date\n            from appointments\n            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime desc ROWS UNBOUNDED PRECEDING)\n        ) as A\n        where second_value is not null and third_value is not null\n          and first_status='New'\n          and second_status='New'\n          and third_status='New'\n        group by subject_identifier, site_id,  first_value, second_value, third_value,\n                 EXTRACT(DAY FROM third_date - first_date),\n                 EXTRACT(DAY FROM now() - first_date),\n                 first_status, second_status, third_status\n        order by subject_identifier, site_id\n    ) as B",
                "unattended_three_in_row2_view",
                engine="django.db.backends.postgresql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\n    with appointments as (\n        select subject_identifier, site_id, visit_code, visit_code_sequence, appt_datetime,\n        case when appt_timing='missed' then 'New' else appt_status end as `appt_status`,\n        case when appt_timing='missed' then 1 else 0 end as `missed`\n        from edc_appointment_appointment\n        where visit_code_sequence=0 and appt_datetime<=now()\n        order by subject_identifier, appt_datetime\n        )\n    SELECT *, lower(\n            hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n            substr(hex( randomblob(2)), 2) || '-' ||\n            substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n            substr(hex(randomblob(2)), 2) || '-' ||\n            hex(randomblob(6))\n          ) as id, datetime() as created, 'meta_reports.unattendedthreeinrow2' as report_model from (\n        select  distinct subject_identifier, site_id,  first_value, second_value, third_value,\n            CAST(JulianDay(third_date) - JulianDay(first_date) AS Integer) as interval_days,\n            CAST(JulianDay(datetime()) - JulianDay(first_date) AS Integer) as from_now_days,\n            first_status, second_status, third_status, sum(missed) as missed_count\n        from (\n            select subject_identifier,site_id,appt_datetime, missed,\n            FIRST_VALUE(appt_status) OVER w as third_status,\n            NTH_VALUE(appt_status, 2) OVER w as second_status,\n            NTH_VALUE(appt_status, 3) OVER w as first_status,\n            FIRST_VALUE(visit_code) OVER w as third_value,\n            NTH_VALUE(visit_code, 2) OVER w as second_value,\n            NTH_VALUE(visit_code, 3) OVER w as first_value,\n            FIRST_VALUE(appt_datetime) OVER w as third_date,\n            NTH_VALUE(appt_datetime, 2) OVER w as second_date,\n            NTH_VALUE(appt_datetime, 3) OVER w as first_date\n            from appointments\n            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime desc ROWS UNBOUNDED PRECEDING)\n        ) as A\n        where second_value is not null and third_value is not null\n          and first_status='New'\n          and second_status='New'\n          and third_status='New'\n        group by subject_identifier, site_id,  first_value, second_value, third_value,\n                 CAST(JulianDay(third_date) - JulianDay(first_date) AS Integer),\n                 CAST(JulianDay(datetime()) - JulianDay(first_date) AS Integer),\n                 first_status, second_status, third_status\n        order by subject_identifier, site_id\n    ) as B",
                "unattended_three_in_row2_view",
                engine="django.db.backends.sqlite3",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "with appointments as (\n        select subject_identifier, site_id, visit_code, visit_code_sequence, appt_datetime,\n        case when appt_timing='missed' then 'New' else appt_status end as `appt_status`,\n        case when appt_timing='missed' then 1 else 0 end as `missed`\n        from edc_appointment_appointment\n        where visit_code_sequence=0 and appt_datetime<=now()\n        order by subject_identifier, appt_datetime\n        )\n    SELECT *, lower(\n            hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n            substr(hex( randomblob(2)), 2) || '-' ||\n            substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n            substr(hex(randomblob(2)), 2) || '-' ||\n            hex(randomblob(6))\n          ) as id, datetime() as created, 'meta_reports.unattendedthreeinrow2' as report_model from (\n        select  distinct subject_identifier, site_id,  first_value, second_value, third_value,\n            CAST(JulianDay(third_date) - JulianDay(first_date) AS Integer) as interval_days,\n            CAST(JulianDay(datetime()) - JulianDay(first_date) AS Integer) as from_now_days,\n            first_status, second_status, third_status, sum(missed) as missed_count\n        from (\n            select subject_identifier,site_id,appt_datetime, missed,\n            FIRST_VALUE(appt_status) OVER w as third_status,\n            NTH_VALUE(appt_status, 2) OVER w as second_status,\n            NTH_VALUE(appt_status, 3) OVER w as first_status,\n            FIRST_VALUE(visit_code) OVER w as third_value,\n            NTH_VALUE(visit_code, 2) OVER w as second_value,\n            NTH_VALUE(visit_code, 3) OVER w as first_value,\n            FIRST_VALUE(appt_datetime) OVER w as third_date,\n            NTH_VALUE(appt_datetime, 2) OVER w as second_date,\n            NTH_VALUE(appt_datetime, 3) OVER w as first_date\n            from appointments\n            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime desc ROWS UNBOUNDED PRECEDING)\n        ) as A\n        where second_value is not null and third_value is not null\n          and first_status='New'\n          and second_status='New'\n          and third_status='New'\n        group by subject_identifier, site_id,  first_value, second_value, third_value,\n                 CAST(JulianDay(third_date) - JulianDay(first_date) AS Integer),\n                 CAST(JulianDay(datetime()) - JulianDay(first_date) AS Integer),\n                 first_status, second_status, third_status\n        order by subject_identifier, site_id\n    ) as B",
                "unattended_three_in_row2_view",
                engine="django.db.backends.sqlite3",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\n    select *, uuid() as `id`, now() as `created`, 'meta_reports.unattendedtwoinrow' as report_model from (\n        select subject_identifier, site_id, appt_datetime, `first_value`, `second_value`,\n            datediff(`second_date`, `first_date`) as `interval_days`,\n            datediff(now(), `first_date`) as `from_now_days`\n            from (\n                select subject_identifier ,site_id, appt_datetime,\n                FIRST_VALUE(`visit_code`) OVER w as `first_value`,\n                NTH_VALUE(`visit_code`, 2) OVER w as `second_value`,\n                NTH_VALUE(`visit_code`, 3) OVER w as `third_value`,\n                FIRST_VALUE(`appt_datetime`) OVER w as `first_date`,\n                NTH_VALUE(`appt_datetime`, 2) OVER w as `second_date`\n                from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n                and appt_datetime <= now()\n                WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n            ) as A1\n        where `second_value` is not null and `third_value` is null\n    ) as A2\n    order by site_id, `from_now_days` desc",
                "unattended_two_in_row_view",
                engine="django.db.backends.mysql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "select *, uuid() as `id`, now() as `created`, 'meta_reports.unattendedtwoinrow' as report_model from (\n        select subject_identifier, site_id, appt_datetime, `first_value`, `second_value`,\n            datediff(`second_date`, `first_date`) as `interval_days`,\n            datediff(now(), `first_date`) as `from_now_days`\n            from (\n                select subject_identifier ,site_id, appt_datetime,\n                FIRST_VALUE(`visit_code`) OVER w as `first_value`,\n                NTH_VALUE(`visit_code`, 2) OVER w as `second_value`,\n                NTH_VALUE(`visit_code`, 3) OVER w as `third_value`,\n                FIRST_VALUE(`appt_datetime`) OVER w as `first_date`,\n                NTH_VALUE(`appt_datetime`, 2) OVER w as `second_date`\n                from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n                and appt_datetime <= now()\n                WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n            ) as A1\n        where `second_value` is not null and `third_value` is null\n    ) as A2\n    order by site_id, `from_now_days` desc",
                "unattended_two_in_row_view",
                engine="django.db.backends.mysql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\n    select *, gen_random_uuid() as id, now() as created, 'meta_reports.unattendedtwoinrow' as report_model\n    from (\n        select subject_identifier, site_id, appt_datetime, first_value, second_value,\n            EXTRACT(DAY FROM second_date - first_date) as interval_days,\n            EXTRACT(DAY FROM now() - first_date) as from_now_days\n            from (\n                select subject_identifier, site_id, appt_datetime,\n                FIRST_VALUE(visit_code) OVER w as first_value,\n                NTH_VALUE(visit_code, 2) OVER w as second_value,\n                NTH_VALUE(visit_code, 3) OVER w as third_value,\n                FIRST_VALUE(appt_datetime) OVER w as first_date,\n                NTH_VALUE(appt_datetime, 2) OVER w as second_date\n                from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n                and appt_datetime <= now()\n                WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n            ) as A1\n        where second_value is not null and third_value is null\n    ) as A2\n    order by site_id, from_now_days desc",
                "unattended_two_in_row_view",
                engine="django.db.backends.postgresql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "select *, gen_random_uuid() as id, now() as created, 'meta_reports.unattendedtwoinrow' as report_model \n    from (\n        select subject_identifier, site_id, appt_datetime, first_value, second_value,\n            EXTRACT(DAY FROM second_date - first_date) as interval_days,\n            EXTRACT(DAY FROM now() - first_date) as from_now_days\n            from (\n                select subject_identifier, site_id, appt_datetime,\n                FIRST_VALUE(visit_code) OVER w as first_value,\n                NTH_VALUE(visit_code, 2) OVER w as second_value,\n                NTH_VALUE(visit_code, 3) OVER w as third_value,\n                FIRST_VALUE(appt_datetime) OVER w as first_date,\n                NTH_VALUE(appt_datetime, 2) OVER w as second_date\n                from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n                and appt_datetime <= now()\n                WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n            ) as A1\n        where second_value is not null and third_value is null\n    ) as A2\n    order by site_id, from_now_days desc",
                "unattended_two_in_row_view",
                engine="django.db.backends.postgresql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "# noqa\nSELECT *, lower(\n    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n    substr(hex( randomblob(2)), 2) || '-' ||\n    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n    substr(hex(randomblob(2)), 2) || '-' ||\n    hex(randomblob(6))\n  ) as id, datetime() as created, 'meta_reports.unattendedtwoinrow' as report_model from (\n        select subject_identifier, site_id, appt_datetime, first_value, second_value,\n            CAST(JulianDay(second_date) - JulianDay(first_date) AS Integer) as interval_days,\n            CAST(JulianDay(datetime()) - JulianDay(first_date) AS Integer) as from_now_days\n            from (\n                select subject_identifier ,site_id, appt_datetime,\n                FIRST_VALUE(visit_code) OVER w as first_value,\n                NTH_VALUE(visit_code, 2) OVER w as second_value,\n                NTH_VALUE(visit_code, 3) OVER w as third_value,\n                FIRST_VALUE(appt_datetime) OVER w as first_date,\n                NTH_VALUE(appt_datetime, 2) OVER w as second_date\n                from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n                and appt_datetime <= datetime()\n                WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n            ) as A1\n        where second_value is not null and third_value is null\n    ) as A2\n    order by site_id, from_now_days desc",
                "unattended_two_in_row_view",
                engine="django.db.backends.sqlite3",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "SELECT *, lower(\n    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||\n    substr(hex( randomblob(2)), 2) || '-' ||\n    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||\n    substr(hex(randomblob(2)), 2) || '-' ||\n    hex(randomblob(6))\n  ) as id, datetime() as created, 'meta_reports.unattendedtwoinrow' as report_model from (\n        select subject_identifier, site_id, appt_datetime, first_value, second_value,\n            CAST(JulianDay(second_date) - JulianDay(first_date) AS Integer) as interval_days,\n            CAST(JulianDay(datetime()) - JulianDay(first_date) AS Integer) as from_now_days\n            from (\n                select subject_identifier ,site_id, appt_datetime,\n                FIRST_VALUE(visit_code) OVER w as first_value,\n                NTH_VALUE(visit_code, 2) OVER w as second_value,\n                NTH_VALUE(visit_code, 3) OVER w as third_value,\n                FIRST_VALUE(appt_datetime) OVER w as first_date,\n                NTH_VALUE(appt_datetime, 2) OVER w as second_date\n                from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'\n                and appt_datetime <= datetime()\n                WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)\n            ) as A1\n        where second_value is not null and third_value is null\n    ) as A2\n    order by site_id, from_now_days desc",
                "unattended_two_in_row_view",
                engine="django.db.backends.sqlite3",
            ),
            atomic=False,
        ),
    ]
