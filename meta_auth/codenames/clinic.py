from copy import copy

from edc_auth.codenames import clinic as default
from sarscov2.auth import sarscov2_codenames

clinic = copy(default)
clinic += [
    "meta_lists.view_arvregimens",
    "meta_lists.view_baselinesymptoms",
    "meta_lists.view_diabetessymptoms",
    "meta_lists.view_offstudyreasons",
    "meta_lists.view_oiprophylaxis",
    "meta_lists.view_symptoms",
    "meta_lists.view_nonadherencereasons",
    "meta_lists.view_subjectvisitmissedreasons",
    "meta_prn.add_endofstudy",
    "meta_prn.add_losstofollowup",
    "meta_prn.add_onschedule",
    "meta_prn.add_protocoldeviationviolation",
    "meta_prn.change_endofstudy",
    "meta_prn.change_losstofollowup",
    "meta_prn.change_onschedule",
    "meta_prn.change_protocoldeviationviolation",
    "meta_prn.delete_endofstudy",
    "meta_prn.delete_losstofollowup",
    "meta_prn.delete_onschedule",
    "meta_prn.delete_protocoldeviationviolation",
    "meta_prn.view_endofstudy",
    "meta_prn.view_historicalendofstudy",
    "meta_prn.view_historicallosstofollowup",
    "meta_prn.view_historicalonschedule",
    "meta_prn.view_historicalprotocoldeviationviolation",
    "meta_prn.view_losstofollowup",
    "meta_prn.view_onschedule",
    "meta_prn.view_protocoldeviationviolation",
    "meta_prn.view_unblindingrequestoruser",
    "meta_prn.view_unblindingrevieweruser",
    "meta_subject.add_bloodresultsfbc",
    "meta_subject.add_bloodresultsglu",
    "meta_subject.add_bloodresultshba1c",
    "meta_subject.add_bloodresultslipid",
    "meta_subject.add_bloodresultslft",
    "meta_subject.add_bloodresultsrft",
    "meta_subject.add_complications",
    "meta_subject.add_followupexamination",
    "meta_subject.add_followupvitals",
    "meta_subject.add_glucose",
    "meta_subject.add_healtheconomics",
    "meta_subject.add_malariatest",
    "meta_subject.add_medicationadherence",
    "meta_subject.add_subjectvisitmissed",
    "meta_subject.add_patienthistory",
    "meta_subject.add_physicalexam",
    "meta_subject.add_subjectrequisition",
    "meta_subject.add_subjectvisit",
    "meta_subject.add_urinedipsticktest",
    "meta_subject.change_bloodresultsfbc",
    "meta_subject.change_bloodresultsglu",
    "meta_subject.change_bloodresultshba1c",
    "meta_subject.change_bloodresultslipid",
    "meta_subject.change_bloodresultslft",
    "meta_subject.change_bloodresultsrft",
    "meta_subject.change_complications",
    "meta_subject.change_followupexamination",
    "meta_subject.change_followupvitals",
    "meta_subject.change_glucose",
    "meta_subject.change_healtheconomics",
    "meta_subject.change_malariatest",
    "meta_subject.change_medicationadherence",
    "meta_subject.change_subjectvisitmissed",
    "meta_subject.change_patienthistory",
    "meta_subject.change_physicalexam",
    "meta_subject.change_subjectrequisition",
    "meta_subject.change_subjectvisit",
    "meta_subject.change_urinedipsticktest",
    "meta_subject.delete_bloodresultsfbc",
    "meta_subject.delete_bloodresultsglu",
    "meta_subject.delete_bloodresultshba1c",
    "meta_subject.delete_bloodresultslipid",
    "meta_subject.delete_bloodresultslft",
    "meta_subject.delete_bloodresultsrft",
    "meta_subject.delete_complications",
    "meta_subject.delete_followupexamination",
    "meta_subject.delete_followupvitals",
    "meta_subject.delete_glucose",
    "meta_subject.delete_healtheconomics",
    "meta_subject.delete_malariatest",
    "meta_subject.delete_medicationadherence",
    "meta_subject.delete_subjectvisitmissed",
    "meta_subject.delete_patienthistory",
    "meta_subject.delete_physicalexam",
    "meta_subject.delete_subjectrequisition",
    "meta_subject.delete_subjectvisit",
    "meta_subject.delete_urinedipsticktest",
    "meta_subject.view_bloodresultsfbc",
    "meta_subject.view_bloodresultsglu",
    "meta_subject.view_bloodresultshba1c",
    "meta_subject.view_bloodresultslipid",
    "meta_subject.view_bloodresultslft",
    "meta_subject.view_bloodresultsrft",
    "meta_subject.view_complications",
    "meta_subject.view_followupexamination",
    "meta_subject.view_followupvitals",
    "meta_subject.view_glucose",
    "meta_subject.view_healtheconomics",
    "meta_subject.view_historicalbloodresultsfbc",
    "meta_subject.view_historicalbloodresultsglu",
    "meta_subject.view_historicalbloodresultshba1c",
    "meta_subject.view_historicalbloodresultslipid",
    "meta_subject.view_historicalbloodresultslft",
    "meta_subject.view_historicalbloodresultsrft",
    "meta_subject.view_historicalcomplications",
    "meta_subject.view_historicalfollowupexamination",
    "meta_subject.view_historicalfollowupvitals",
    "meta_subject.view_historicalglucose",
    "meta_subject.view_historicalhealtheconomics",
    "meta_subject.view_historicalmalariatest",
    "meta_subject.view_historicalmedicationadherence",
    "meta_subject.view_historicalsubjectvisitmissed",
    "meta_subject.view_historicalpatienthistory",
    "meta_subject.view_historicalphysicalexam",
    "meta_subject.view_historicalsubjectrequisition",
    "meta_subject.view_historicalsubjectvisit",
    "meta_subject.view_historicalurinedipsticktest",
    "meta_subject.view_malariatest",
    "meta_subject.view_medicationadherence",
    "meta_subject.view_subjectvisitmissed",
    "meta_subject.view_patienthistory",
    "meta_subject.view_physicalexam",
    "meta_subject.view_subjectrequisition",
    "meta_subject.view_subjectvisit",
    "meta_subject.view_urinedipsticktest",
]
clinic.extend(sarscov2_codenames)
clinic.sort()
