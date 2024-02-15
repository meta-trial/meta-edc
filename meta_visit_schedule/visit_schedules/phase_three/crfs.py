from edc_visit_schedule.visit import Crf, CrfCollection

crfs_prn = CrfCollection(
    Crf(show_order=105, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=156, model="meta_subject.glucose"),
    Crf(show_order=225, model="meta_subject.glucosefbg"),
    Crf(show_order=235, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=245, model="meta_subject.bloodresultsrft"),
    Crf(show_order=255, model="meta_subject.bloodresultslft"),
    Crf(show_order=265, model="meta_subject.bloodresultslipid"),
    Crf(show_order=275, model="meta_subject.hepatitistest"),
    Crf(show_order=285, model="meta_subject.malariatest"),
    Crf(show_order=295, model="meta_subject.urinedipsticktest"),
    Crf(show_order=365, model="meta_subject.concomitantmedication"),
    Crf(show_order=385, model="meta_subject.urinepregnancy"),
    Crf(show_order=505, model="meta_subject.pregnancyupdate"),
    Crf(show_order=515, model="meta_subject.egfrdropnotification"),
    Crf(show_order=615, model="meta_subject.dmreferralfollowup"),
    name="prn",
)

crfs_unscheduled = CrfCollection(
    Crf(show_order=106, model="meta_subject.followupvitals"),
    Crf(show_order=206, model="meta_subject.followupexamination"),
    Crf(show_order=306, model="meta_subject.medicationadherence"),
    Crf(show_order=406, model="meta_subject.glucosefbg"),
    name="unscheduled",
)

crfs_missed = CrfCollection(
    Crf(show_order=107, model="meta_subject.subjectvisitmissed"),
    name="missed",
)
crfs_d1 = CrfCollection(
    Crf(show_order=100, model="meta_subject.physicalexam"),
    Crf(show_order=120, model="meta_subject.patienthistory"),
    Crf(show_order=130, model="meta_subject.otherarvregimens"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=210, model="meta_subject.bloodresultsins"),
    Crf(show_order=220, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=230, model="meta_subject.bloodresultsrft"),
    Crf(show_order=240, model="meta_subject.bloodresultslft"),
    Crf(show_order=250, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=260, model="meta_subject.bloodresultslipid"),
    Crf(show_order=360, model="meta_subject.malariatest"),
    Crf(show_order=370, model="meta_subject.urinedipsticktest"),
    Crf(show_order=400, model="meta_subject.studymedication"),
    name="day1",
)

crfs_w2 = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=200, model="meta_subject.glucosefbg"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l"),
    Crf(show_order=465, model="meta_subject.sf12"),
    Crf(show_order=470, model="meta_subject.healtheconomicssimple"),
    name="week2",
)

crfs_1m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=200, model="meta_subject.glucosefbg"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=450, model="meta_subject.healtheconomicssimple", required=False),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    Crf(show_order=470, model="meta_subject.mnsi"),
    name="1m",
)

crfs_3m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=200, model="meta_subject.glucosefbg"),
    Crf(show_order=210, model="meta_subject.bloodresultsrft"),
    Crf(show_order=220, model="meta_subject.bloodresultslft"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    Crf(show_order=470, model="meta_subject.mnsi", required=False),
    name="3m",
)

crfs_6m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.glucose", required=False),
    Crf(show_order=205, model="meta_subject.glucosefbg"),
    Crf(show_order=210, model="meta_subject.bloodresultsrft"),
    Crf(show_order=220, model="meta_subject.bloodresultslft"),
    Crf(show_order=230, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    Crf(show_order=470, model="meta_subject.mnsi", required=False),
    name="6m",
)

crfs_9m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=200, model="meta_subject.glucosefbg"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    name="9m",
)

crfs_12m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose"),
    Crf(show_order=210, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=220, model="meta_subject.bloodresultsrft"),
    Crf(show_order=230, model="meta_subject.bloodresultslft"),
    Crf(show_order=240, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=250, model="meta_subject.bloodresultslipid"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    name="12m",
)

crfs_15m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=200, model="meta_subject.glucosefbg"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    name="15m",
)

crfs_18m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=205, model="meta_subject.glucosefbg"),
    Crf(show_order=220, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    name="18m",
)

crfs_21m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=200, model="meta_subject.glucosefbg"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    name="21m",
)

crfs_24m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.glucose"),
    Crf(show_order=210, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=220, model="meta_subject.bloodresultsrft"),
    Crf(show_order=230, model="meta_subject.bloodresultslft"),
    Crf(show_order=240, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=250, model="meta_subject.bloodresultslipid"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    name="24m",
)

crfs_27m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=200, model="meta_subject.glucosefbg"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    name="27m",
)

crfs_30m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=205, model="meta_subject.glucosefbg"),
    Crf(show_order=210, model="meta_subject.bloodresultsrft"),
    Crf(show_order=220, model="meta_subject.bloodresultslft"),
    Crf(show_order=230, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    name="30m",
)

crfs_33m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=155, model="meta_subject.glucose", required=False),
    Crf(show_order=200, model="meta_subject.glucosefbg"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    name="33m",
)

crfs_36m = CrfCollection(
    Crf(show_order=100, model="meta_subject.followupvitals"),
    Crf(show_order=150, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.glucose"),
    Crf(show_order=210, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=220, model="meta_subject.bloodresultsrft"),
    Crf(show_order=230, model="meta_subject.bloodresultslft"),
    Crf(show_order=240, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=250, model="meta_subject.bloodresultslipid"),
    Crf(show_order=300, model="meta_subject.studymedication"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=460, model="meta_subject.eq5d3l", required=False),
    Crf(show_order=465, model="meta_subject.sf12", required=False),
    name="36m",
)
