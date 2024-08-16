mysql_view = """ # noqa
    select *, uuid() as `id`, now() as `created`, 'meta_reports.unattendedtwoinrow' as report_model from (
        select subject_identifier, site_id, appt_datetime, `first_value`, `second_value`,
            datediff(`second_date`, `first_date`) as `interval_days`,
            datediff(now(), `first_date`) as `from_now_days`
            from (
                select subject_identifier ,site_id, appt_datetime,
                FIRST_VALUE(`visit_code`) OVER w as `first_value`,
                NTH_VALUE(`visit_code`, 2) OVER w as `second_value`,
                NTH_VALUE(`visit_code`, 3) OVER w as `third_value`,
                FIRST_VALUE(`appt_datetime`) OVER w as `first_date`,
                NTH_VALUE(`appt_datetime`, 2) OVER w as `second_date`
                from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'
                and appt_datetime <= now()
                WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)
            ) as A1
        where `second_value` is not null and `third_value` is null
    ) as A2
    order by site_id, `from_now_days` desc
"""

pg_view = """ # noqa
    select *, gen_random_uuid() as id, now() as created, 'meta_reports.unattendedtwoinrow' as report_model
    from (
        select subject_identifier, site_id, appt_datetime, first_value, second_value,
            EXTRACT(DAY FROM second_date - first_date) as interval_days,
            EXTRACT(DAY FROM now() - first_date) as from_now_days
            from (
                select subject_identifier, site_id, appt_datetime,
                FIRST_VALUE(visit_code) OVER w as first_value,
                NTH_VALUE(visit_code, 2) OVER w as second_value,
                NTH_VALUE(visit_code, 3) OVER w as third_value,
                FIRST_VALUE(appt_datetime) OVER w as first_date,
                NTH_VALUE(appt_datetime, 2) OVER w as second_date
                from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'
                and appt_datetime <= now()
                WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)
            ) as A1
        where second_value is not null and third_value is null
    ) as A2
    order by site_id, from_now_days desc
"""

sqlite3_view = """  # noqa
SELECT *, lower(
    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||
    substr(hex( randomblob(2)), 2) || '-' ||
    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||
    substr(hex(randomblob(2)), 2) || '-' ||
    hex(randomblob(6))
  ) as id, datetime() as created, 'meta_reports.unattendedtwoinrow' as report_model from (
        select subject_identifier, site_id, appt_datetime, first_value, second_value,
            CAST(JulianDay(second_date) - JulianDay(first_date) AS Integer) as interval_days,
            CAST(JulianDay(datetime()) - JulianDay(first_date) AS Integer) as from_now_days
            from (
                select subject_identifier ,site_id, appt_datetime,
                FIRST_VALUE(visit_code) OVER w as first_value,
                NTH_VALUE(visit_code, 2) OVER w as second_value,
                NTH_VALUE(visit_code, 3) OVER w as third_value,
                FIRST_VALUE(appt_datetime) OVER w as first_date,
                NTH_VALUE(appt_datetime, 2) OVER w as second_date
                from edc_appointment_appointment where visit_code_sequence=0 and appt_status='New'
                and appt_datetime <= datetime()
                WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)
            ) as A1
        where second_value is not null and third_value is null
    ) as A2
    order by site_id, from_now_days desc
"""


def get_view_definition() -> dict:
    return {
        "django.db.backends.mysql": mysql_view,
        "django.db.backends.postgresql": pg_view,
        "django.db.backends.sqlite3": sqlite3_view,
    }
