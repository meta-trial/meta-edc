create view unattended_three_in_row2_view as (
    with appointments as (
        select `subject_identifier`, `site_id`, `visit_code`, `visit_code_sequence`, `appt_datetime`,
        case when `appt_timing`='missed' then 'New' else `appt_status` end as 'appt_status',
        case when `appt_timing`='missed' then 1 else 0 end as 'missed'
        from edc_appointment_appointment
        where `visit_code_sequence`=0 and appt_datetime<=now()
        order by subject_identifier, appt_datetime
        )
    select *, uuid() as 'id', now() as 'created', 'meta_reports.unattendedthreeinrow2' as report_model from (
        select  distinct `subject_identifier`, `site_id`,  `first`, `second`, `third`,
            datediff(`third_date`, `first_date`) as 'interval_days',
            datediff(now(), `first_date`) as 'from_now_days',
            `first_status`, `second_status`, `third_status`, sum(`missed`) as `missed_count`
        from (
            select `subject_identifier`,`site_id`,`appt_datetime`, `missed`,
            FIRST_VALUE(`appt_status`) OVER w as 'third_status',
            NTH_VALUE(`appt_status`, 2) OVER w as 'second_status',
            NTH_VALUE(`appt_status`, 3) OVER w as 'first_status',
            FIRST_VALUE(`visit_code`) OVER w as 'third',
            NTH_VALUE(`visit_code`, 2) OVER w as 'second',
            NTH_VALUE(`visit_code`, 3) OVER w as 'first',
            FIRST_VALUE(`appt_datetime`) OVER w as 'third_date',
            NTH_VALUE(`appt_datetime`, 2) OVER w as 'second_date',
            NTH_VALUE(`appt_datetime`, 3) OVER w as 'first_date'
            from appointments
            WINDOW w as (PARTITION BY `subject_identifier` order by `appt_datetime` desc ROWS UNBOUNDED PRECEDING)
        ) as A
        where `second` is not null and `third` is not null
          and `first_status`='New'
          and `second_status`='New'
          and `third_status`='New'
        group by `subject_identifier`, `site_id`,  `first`, `second`, `third`,
                 datediff(`third_date`, `first_date`),
                 datediff(now(), `first_date`),
                 `first_status`, `second_status`, `third_status`
        order by `subject_identifier`, `site_id`
    ) as B
);