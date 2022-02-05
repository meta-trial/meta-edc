from edc_constants.constants import DEAD, NONE, OTHER, UNKNOWN
from edc_ltfu.constants import LOST_TO_FOLLOWUP
from edc_transfer.constants import TRANSFERRED

from meta_edc.meta_version import PHASE_THREE, get_meta_version
from meta_prn.constants import LATE_EXCLUSION, OTHER_RX_DISCONTINUATION, WITHDRAWAL

list_data = {
    "meta_lists.abnormalfootappearanceobservations": [
        ("deformities", "Deformities"),
        ("dry_skin_callus", "Dry skin, callus"),
        ("infection", "Infection"),
        ("fissure", "Fissure"),
        (OTHER, "Other abnormality, please specify"),
    ],
    "meta_lists.nonadherencereasons": [
        ("forget_to_take", "I sometimes forget to take my pills"),
        ("dont_like_taking", "I don't like taking my pills"),
        ("make_me_ill", "My pills sometimes make me feel sick"),
        ("misplaced_pills", "I sometimes misplace my pills"),
        ("dont_believe_pills_help", "I don't believe my pills are helping me"),
        ("dont_believe_pills_needed", "I don't believe I need to take my pills"),
        ("not_feeling_well", "I have not been feeling well"),
        (OTHER, "Other, please specify ..."),
    ],
    "meta_lists.hypertensionmedications": [
        ("amlodipine", "Amlodipine"),
        ("atenolol", "Atenolol"),
        ("bendroflumethiazide", "Bendroflumethiazide"),
        ("bisoprolol", "Bisoprolol"),
        ("captopril", "Captopril"),
        ("diltiazem", "Diltiazem"),
        ("enalapril", "Enalapril"),
        ("eplerenone", "Eplerenone"),
        ("furosemide", "Furosemide"),
        ("hydralazine", "Hydralazine"),
        ("hydrochlothiazide", "Hydrochlothiazide"),
        ("indapamide", "Indapamide"),
        ("losartan", "Losartan"),
        ("metoprolol", "Metoprolol"),
        ("nifedipine", "Nifedipine"),
        ("perindopril", "Perindopril"),
        ("propanolol", "Propanolol"),
        ("spironolactone", "Spironolactone"),
        ("telmisartan", "Telmisartan"),
        ("torsemide", "Torsemide"),
        ("verapamil", "Verapamil"),
        (OTHER, "Other, specify"),
    ],
    "meta_lists.diabetessymptoms": [
        ("frequent_urination", "Wanting to urinate more often than usual"),
        ("excessive_thirst", "Wanting to drink water more than usual"),
        ("excessive_eating", "Wanting to eat food more than usual"),
        (OTHER, "Other, specify"),
        (NONE, "No symptoms to report"),
    ],
    "meta_lists.oiprophylaxis": [
        ("tmp_smx", "TMP/SMX"),
        ("fluconazole", "Fluconazole"),
        ("isoniazid", "Isoniazid"),
        (OTHER, "Other, specify"),
    ],
    "meta_lists.symptoms": [
        (NONE, "--No symptoms to report"),
        ("abdominal_pain_general", "Abdominal pain (General)"),
        ("abdominal_pain_right_upper_quad", "Abdominal pain (Right upper quadrant)"),
        ("blurred_vision", "Blurred vision"),
        ("diarrhoea", "Diarrhoea"),
        ("dizziness", "Dizziness"),
        ("fatigue", "Fatigue"),
        ("flatulence", "Flatulence (gas)"),
        ("headaches", "Headaches"),
        ("increased_appetite", "Increased appetite"),
        ("joint_pain", "Joint pain"),
        ("loss_of_appetite", "Loss of appetite"),
        ("muscle_cramping", "Muscle cramping"),
        ("muscle_pain", "Muscle pain"),
        ("nausea", "Nausea"),
        ("pain_feet_or_lower_limbs", "Pain in feet/lower limbs"),
        ("pounding_heartbeat", "Fast or pounding heartbeat"),
        ("rash", "Rash"),
        ("shakiness", "Shakiness"),
        ("shallow_breathing", "Fast or shallow breathing"),
        ("skin_itching", "Skin itching"),
        ("sweating", "Sweating"),
        ("swelling_feet_or_lower_limbs", "Swelling of feet/lower limbs"),
        ("unusual_sleepiness", "Unusual sleepiness"),
        ("vomiting", "Vomiting"),
        ("weakness", "Weakness"),
        (OTHER, "Other, specify"),
    ],
    "meta_lists.baselinesymptoms": [
        ("abdominal_pain_general", "Abdominal pain (General)"),
        ("cough", "Cough"),
        ("diarrhoea", "Diarrhoea"),
        ("dizziness", "Dizziness"),
        ("fatigue", "Fatigue"),
        ("headaches", "Headaches"),
        ("loss_of_appetite", "Loss of appetite"),
        ("loss_of_weight", "Loss of weight"),
        ("muscle_cramping", "Muscle cramping"),
        ("shakiness", "Shakiness"),
        ("shallow_breathing", "Fast or shallow breathing"),
        ("skin_infection", "Skin infection"),
        ("sweating", "Sweating"),
        ("unusual_sleepiness", "Unusual sleepiness"),
        ("vomiting", "Vomiting"),
        ("weakness", "Weakness"),
        (NONE, "No symptoms to report"),
        (OTHER, "Other, specify"),
    ],
    "meta_lists.arvregimens": [
        ("ABC_3TC_ATV_r", "ABC + 3TC + ATV/r"),
        ("ABC_3TC_LPV_r", "ABC + 3TC + LPV/r"),
        ("AZT_3TC_ATV_r", "AZT + 3TC + ATV/r"),
        ("AZT_3TC_EFV", "AZT + 3TC + EFV"),
        ("AZT_3TC_LPV_r", "AZT + 3TC + LPV/r"),
        ("AZT_3TC_NVP", "AZT + 3TC + NVP"),
        ("D4T_3TC_NVP", "D4T + 3TC + NVP"),
        ("DTG_ABC/3TC_ATV_r", "DTG + (ABC/3TC) + ATV/r"),
        ("TDF_3TC_ATV_r", "TDF + 3TC + ATV/r"),
        ("TDF_3TC_DTG", "TDF + 3TC + DTG"),
        ("TDF_3TC_EFV", "TDF + 3TC + EFV"),
        ("TDF_3TC_LPV_r", "TDF + 3TC + LPV/r"),
        ("TDF_FTC_ATV_r", "TDF + FTC + ATV/r"),
        ("TDF_FTC_EFV", "TDF + FTC + EFV"),
        ("TDF_FTC_LPV_r", "TDF + FTC + LPV/r"),
        ("ZDV_3TC_EFV", "ZDV + 3TC + EFV"),
        ("ZDV_3TC_NVP", "ZDV + 3TC + NVP"),
        ("ZDV_LPV_NVP", "ZDV + LPV + NVP"),
        (UNKNOWN, "Unknown"),
        (OTHER, "Other, specify ..."),
    ],
    "meta_lists.offstudyreasons": [
        ("completed_followup", "Patient completed 36 months of follow-up"),
        ("diabetes", "Patient developed diabetes"),
        ("clinical_withdrawal", "Patient is withdrawn on CLINICAL grounds ..."),
        ("", ""),
        ("clinical_endpoint", "Patient reached a clinical endpoint"),
        ("toxicity", "Patient experienced an unacceptable toxicity"),
        (
            "intercurrent_illness",
            "Intercurrent illness which prevents further treatment",
        ),
        (LOST_TO_FOLLOWUP, "Patient lost to follow-up"),
        (DEAD, "Patient reported/known to have died"),
        (WITHDRAWAL, "Patient withdrew consent to participate further"),
        (LATE_EXCLUSION, "Patient fulfilled late exclusion criteria*"),
        (TRANSFERRED, "Patient has been transferred to another health centre"),
        (
            OTHER_RX_DISCONTINUATION,
            "Other condition that justifies the discontinuation of "
            "treatment in the clinician’s opinion (specify below)",
        ),
        (
            OTHER,
            "Other reason (specify below)",
        ),
    ],
    "meta_lists.subjectvisitmissedreasons": [
        ("forgot", "Forgot / Can’t remember being told about appointment"),
        ("family_emergency", "Family emergency (e.g. funeral) and was away"),
        ("travelling", "Away travelling/visiting"),
        ("working_schooling", "Away working/schooling"),
        ("too_sick", "Too sick or weak to come to the centre"),
        ("lack_of_transport", "Transportation difficulty"),
        (OTHER, "Other reason (specify below)"),
    ],
}
if get_meta_version() == PHASE_THREE:
    # TODO: customize for META PHASE THREE. see updated EoS form for the reasons
    """
    4 = Patient experienced an unacceptable toxicity
        A = Development of lactic acidosis or hyperlactatemia
        B = Development of hepatomegaly with steatosis
        C = Other (specify below)
    """

    list_data.update(
        {
            "meta_lists.offstudyreasons": [
                ("completed_followup", "Patient completed 36 months of follow-up"),
                ("diabetes", "Patient developed diabetes"),
                ("clinical_withdrawal", "Patient is withdrawn on CLINICAL grounds ..."),
                (
                    "toxicity",
                    "Patient experienced an unacceptable toxicity, specify below ...",
                ),
                ("clinical_endpoint", "Patient reached a clinical endpoint"),
                ("toxicity", "Patient experienced an unacceptable toxicity"),
                (
                    "intercurrent_illness",
                    "Intercurrent illness which prevents further treatment",
                ),
                (LOST_TO_FOLLOWUP, "Patient lost to follow-up"),
                (DEAD, "Patient reported/known to have died"),
                (WITHDRAWAL, "Patient withdrew consent to participate further"),
                (
                    LATE_EXCLUSION,
                    (
                        "Patient fulfilled late exclusion criteria (due to abnormal "
                        "blood values or raised blood pressure at enrolment"
                    ),
                ),
                (TRANSFERRED, "Patient has been transferred to another health centre"),
                (OTHER, "Other reason (specify below)"),
            ]
        }
    )
