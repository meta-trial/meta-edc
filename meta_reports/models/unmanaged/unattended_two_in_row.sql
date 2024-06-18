create view unattended_two_in_row_view as (
    select *, uuid() as 'id', now() as 'created', 'meta_reports.unattendedtwoinrow' as report_model from (
        select `subject_identifier`, `site_id`, `appt_datetime`, `first`, `second`,
            datediff(`second_date`, `first_date`) as 'interval_days',
            datediff(now(), `first_date`) as 'from_now_days'
            from (
                select `subject_identifier`,`site_id`,`appt_datetime`,
                FIRST_VALUE(`visit_code`) OVER w as 'first',
                NTH_VALUE(`visit_code`, 2) OVER w as 'second',
                NTH_VALUE(`visit_code`, 3) OVER w as 'third',
                FIRST_VALUE(`appt_datetime`) OVER w as 'first_date',
                NTH_VALUE(`appt_datetime`, 2) OVER w as 'second_date'
                from edc_appointment_appointment where `visit_code_sequence`=0 and `appt_status`='New'
                and `appt_datetime` <= now()
                WINDOW w as (PARTITION BY `subject_identifier` order by `appt_datetime` ROWS UNBOUNDED PRECEDING)
            ) as A1
        where `second` is not null and `third` is null
    ) as A2
    order by `site_id`, `from_now_days` desc);