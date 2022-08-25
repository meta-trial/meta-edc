from edc_auth.get_clinic_codenames import get_clinic_codenames

clinic_codenames = get_clinic_codenames(
    "meta_prn", "meta_subject", "meta_consent", list_app="meta_lists"
)

screening_codenames = [
    "meta_screening.add_screeningpartone",
    "meta_screening.add_screeningpartthree",
    "meta_screening.add_screeningparttwo",
    "meta_screening.add_subjectrefusal",
    "meta_screening.change_screeningpartone",
    "meta_screening.change_screeningpartthree",
    "meta_screening.change_screeningparttwo",
    "meta_screening.change_subjectrefusal",
    "meta_screening.delete_screeningpartone",
    "meta_screening.delete_screeningpartthree",
    "meta_screening.delete_screeningparttwo",
    "meta_screening.delete_subjectrefusal",
    "meta_screening.view_historicalscreeningpartone",
    "meta_screening.view_historicalscreeningpartthree",
    "meta_screening.view_historicalscreeningparttwo",
    "meta_screening.view_historicalsubjectscreening",
    "meta_screening.view_historicalsubjectrefusal",
    "meta_screening.view_screeningpartone",
    "meta_screening.view_screeningpartthree",
    "meta_screening.view_screeningparttwo",
    "meta_screening.view_subjectscreening",
    "meta_screening.view_subjectrefusal",
]
screening_codenames.sort()

ae_local_reviewer = [
    "meta_subject.add_aelocalreview",
    "meta_subject.change_aelocalreview",
    "meta_subject.delete_aelocalreview",
    "meta_subject.view_aelocalreview",
    "meta_subject.view_historicalaelocalreview",
]
ae_sponsor_reviewer = [
    "meta_subject.add_aesponsorreview",
    "meta_subject.change_aesponsorreview",
    "meta_subject.delete_aesponsorreview",
    "meta_subject.view_aesponsorreview",
    "meta_subject.view_historicalaesponsorreview",
]
