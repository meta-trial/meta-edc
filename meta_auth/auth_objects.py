from edc_auth.get_clinic_codenames import get_clinic_codenames

clinic_codenames = get_clinic_codenames(
    "meta_prn", "meta_subject", "meta_consent", list_app="meta_lists"
)


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
