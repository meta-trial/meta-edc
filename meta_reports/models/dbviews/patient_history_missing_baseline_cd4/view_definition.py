mysql_view: str = """
    select *, uuid() as id, now() as created,
    'meta_reports.patienthistorymissingbaselinecd4' as report_model
      from (
        select subject_identifier, v.visit_code, v.visit_code_sequence,cd4,
          cd4_date, crf.site_id, crf.user_created, crf.user_modified,
          crf.modified
        from meta_subject_patienthistory as crf
        left join meta_subject_subjectvisit as v on crf.subject_visit_id=v.id
        where cd4 is null or cd4_date is null
    ) as A
    order by subject_identifier
    """

pg_view: str = """
    select *, get_random_uuid() as id, now() as created,
    'meta_reports.patienthistorymissingbaselinecd4' as report_model
      from (
        select subject_identifier, v.visit_code, v.visit_code_sequence,cd4,
          cd4_date, crf.site_id, crf.user_created, crf.user_modified,
          crf.modified
        from meta_subject_patienthistory as crf
        left join meta_subject_subjectvisit as v on crf.subject_visit_id=v.id
        where cd4 is null or cd4_date is null
    ) as A
    order by subject_identifier
"""

sqlite3_view = """
SELECT *, lower(
    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||
    substr(hex( randomblob(2)), 2) || '-' ||
    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||
    substr(hex(randomblob(2)), 2) || '-' ||
    hex(randomblob(6))
  ) as id, datetime() as `created`,
  'meta_reports.patienthistorymissingbaselinecd4' as report_model
      from (
        select subject_identifier, v.visit_code, v.visit_code_sequence,cd4,
          cd4_date, crf.site_id, crf.user_created, crf.user_modified,
          crf.modified
        from meta_subject_patienthistory as crf
        left join meta_subject_subjectvisit as v on crf.subject_visit_id=v.id
        where cd4 is null or cd4_date is null
    ) as A
    order by subject_identifier
"""


def get_view_definition() -> dict:
    return {
        "django.db.backends.mysql": mysql_view,
        "django.db.backends.postgresql": pg_view,
        "django.db.backends.sqlite3": sqlite3_view,
    }
