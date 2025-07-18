# Generated by Django 6.0 on 2025-04-22 19:32

import django_db_views.migration_functions
import django_db_views.operations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0057_auto_20250422_2224"),
    ]

    operations = [
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "select *, uuid() as id, now() as `created`, 'meta_reports.glucosesummaryview' as `report_model` from (SELECT v.subject_identifier, fbg_value, fbg_units, fbg_datetime, NULL AS `ogtt_value`, NULL AS `ogtt_units`, NULL AS `ogtt_datetime`, CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS `fasted`, fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucosefbg' AS source FROM meta_subject_glucosefbg AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier UNION SELECT v.subject_identifier, fbg_value, fbg_units, fbg_datetime, ogtt_value, ogtt_units, ogtt_datetime, CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS `fasted`, fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucose' AS source FROM meta_subject_glucose AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier) as A ORDER BY subject_identifier, site_id",
                "meta_reports_glucosesummaryview",
                engine="django.db.backends.mysql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "select *, uuid() as id, now() as `created`, 'meta_reports.glucosesummaryview' as `report_model` from (SELECT v.subject_identifier, fbg_value, fbg_datetime, NULL AS `ogtt_value`, NULL AS `ogtt_datetime`, CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS `fasted`, fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucosefbg' AS source FROM meta_subject_glucosefbg AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier UNION SELECT v.subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime, CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS `fasted`, fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucose' AS source FROM meta_subject_glucose AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier) as A ORDER BY subject_identifier, site_id",
                "meta_reports_glucosesummaryview",
                engine="django.db.backends.mysql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "select *, get_random_uuid() as id, now() as created, 'meta_reports.glucosesummaryview' as report_model from (SELECT v.subject_identifier, fbg_value, fbg_units, fbg_datetime, NULL AS \"ogtt_value\", NULL AS \"ogtt_units\", NULL AS \"ogtt_datetime\", CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS \"fasted\", fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucosefbg' AS source FROM meta_subject_glucosefbg AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier UNION SELECT v.subject_identifier, fbg_value, fbg_units, fbg_datetime, ogtt_value, ogtt_units, ogtt_datetime, CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS \"fasted\", fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucose' AS source FROM meta_subject_glucose AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier) as A ORDER BY subject_identifier, site_id",
                "meta_reports_glucosesummaryview",
                engine="django.db.backends.postgresql",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "select *, get_random_uuid() as id, now() as created, 'meta_reports.glucosesummaryview' as report_model from (SELECT v.subject_identifier, fbg_value, fbg_datetime, NULL AS \"ogtt_value\", NULL AS \"ogtt_datetime\", CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS \"fasted\", fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucosefbg' AS source FROM meta_subject_glucosefbg AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier UNION SELECT v.subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime, CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS \"fasted\", fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucose' AS source FROM meta_subject_glucose AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier) as A ORDER BY subject_identifier, site_id",
                "meta_reports_glucosesummaryview",
                engine="django.db.backends.postgresql",
            ),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration(
                "select *, uuid() as id, datetime() as created, 'meta_reports.glucosesummaryview' as report_model from (SELECT v.subject_identifier, fbg_value, fbg_units, fbg_datetime, NULL AS \"ogtt_value\", NULL AS \"ogtt_units\", NULL AS \"ogtt_datetime\", CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS \"fasted\", fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucosefbg' AS source FROM meta_subject_glucosefbg AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier UNION SELECT v.subject_identifier, fbg_value, fbg_units, fbg_datetime, ogtt_value, ogtt_units, ogtt_datetime, CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS \"fasted\", fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucose' AS source FROM meta_subject_glucose AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier) as A ORDER BY subject_identifier, site_id",
                "meta_reports_glucosesummaryview",
                engine="django.db.backends.sqlite3",
            ),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration(
                "select *, uuid() as id, datetime() as created, 'meta_reports.glucosesummaryview' as report_model from (SELECT v.subject_identifier, fbg_value, fbg_datetime, NULL AS \"ogtt_value\", NULL AS \"ogtt_datetime\", CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS \"fasted\", fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucosefbg' AS source FROM meta_subject_glucosefbg AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier UNION SELECT v.subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime, CASE WHEN fasting = 'fasting' THEN 'Yes' WHEN fasting = 'non_fasting' THEN 'No' ELSE fasting END AS \"fasted\", fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime, fasting_duration_delta, 'meta_subject.glucose' AS source FROM meta_subject_glucose AS fbg LEFT JOIN meta_subject_subjectvisit AS v ON v.id = fbg.subject_visit_id LEFT JOIN meta_prn_endofstudy AS eos ON v.subject_identifier = eos.subject_identifier) as A ORDER BY subject_identifier, site_id",
                "meta_reports_glucosesummaryview",
                engine="django.db.backends.sqlite3",
            ),
            atomic=False,
        ),
    ]
