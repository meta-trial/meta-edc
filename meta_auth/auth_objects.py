from django.conf import settings
from edc_auth.get_app_codenames import get_app_codenames

META_REPORTS = "META_REPORTS"
META_REPORTS_AUDIT = "META_REPORTS_AUDIT"
META_PHARMACIST = "META_PHARMACIST"


clinic_codenames = get_app_codenames(
    "meta_prn", "meta_subject", "meta_consent", list_app="meta_lists"
)

reports_codenames = get_app_codenames("meta_reports")
reports_codenames.remove("meta_reports.view_impsubstitutions")

meta_pharmacy_codenames = get_app_codenames("meta_pharmacy")
meta_pharmacy_codenames.extend(get_app_codenames("django_pylabels"))
meta_pharmacy_codenames.append("meta_reports.view_impsubstitutions")
meta_pharmacy_codenames.append("meta_reports.viewallsites_impsubstitutions")
excluded_meta_pharmacy_codenames = [
    "meta_pharmacy.add_rx",
    "meta_pharmacy.change_rx",
    "meta_pharmacy.delete_rx",
]

meta_pharmacy_codenames = [
    c for c in meta_pharmacy_codenames if c not in excluded_meta_pharmacy_codenames
]

add_perms = []
if not settings.LIVE_SYSTEM:
    add_perms = [
        "meta_screening.add_screeningpartone",
        "meta_screening.add_screeningpartthree",
        "meta_screening.add_screeningparttwo",
    ]

screening_codenames = [
    *add_perms,
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
