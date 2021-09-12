from edc_visit_schedule import Crf, FormsCollection

# TODO: whats the diffeence between bloodresultsglu and glucose??
crfs_prn = FormsCollection(
    Crf(show_order=10, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=220, model="meta_subject.bloodresultsglu"),
    Crf(show_order=230, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=240, model="meta_subject.bloodresultsrft"),
    Crf(show_order=250, model="meta_subject.bloodresultslft"),
    Crf(show_order=260, model="meta_subject.bloodresultslipid"),
    Crf(show_order=270, model="meta_subject.hepatitistest"),
    Crf(show_order=280, model="meta_subject.malariatest"),
    Crf(show_order=290, model="meta_subject.urinedipsticktest"),
    Crf(show_order=360, model="meta_subject.mnsi"),
    Crf(show_order=370, model="meta_subject.healtheconomicssimple"),
    name="prn",
)

crfs_unscheduled = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=20, model="meta_subject.followupexamination"),
    Crf(show_order=30, model="meta_subject.medicationadherence"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    name="unscheduled",
)

crfs_missed = FormsCollection(
    Crf(show_order=10, model="meta_subject.subjectvisitmissed"),
    name="missed",
)
crfs_d1 = FormsCollection(
    Crf(show_order=10, model="meta_subject.physicalexam"),
    Crf(show_order=20, model="meta_subject.patienthistory"),
    Crf(show_order=30, model="meta_subject.otherarvregimens"),
    Crf(show_order=210, model="meta_subject.bloodresultsins"),
    Crf(show_order=220, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=230, model="meta_subject.bloodresultsrft"),
    Crf(show_order=240, model="meta_subject.bloodresultslft"),
    Crf(show_order=250, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=260, model="meta_subject.bloodresultslipid"),
    Crf(show_order=360, model="meta_subject.malariatest"),
    Crf(show_order=370, model="meta_subject.urinedipsticktest"),
    Crf(show_order=400, model="meta_subject.studydrugrefill"),
    Crf(show_order=500, model="meta_subject.hepatitistest"),
    name="day1",
)

# TODO: add eq5d to the 2 week visit
crfs_w2 = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=450, model="meta_subject.healtheconomicssimple"),
    Crf(show_order=500, model="meta_subject.hepatitistest", required=False),
    name="week2",
)

crfs_1m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    Crf(show_order=450, model="meta_subject.healtheconomicssimple", required=False),
    Crf(show_order=470, model="meta_subject.mnsi"),
    Crf(show_order=500, model="meta_subject.hepatitistest", required=False),
    name="1m",
)

crfs_3m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=210, model="meta_subject.bloodresultsrft"),
    Crf(show_order=220, model="meta_subject.bloodresultslft"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="3m",
)

crfs_6m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=210, model="meta_subject.bloodresultsrft"),
    Crf(show_order=220, model="meta_subject.bloodresultslft"),
    Crf(show_order=230, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="6m",
)

crfs_9m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="9m",
)

crfs_12m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.glucose"),
    Crf(show_order=210, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=220, model="meta_subject.bloodresultsrft"),
    Crf(show_order=230, model="meta_subject.bloodresultslft"),
    Crf(show_order=240, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=250, model="meta_subject.bloodresultslipid"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="12m",
)

crfs_15m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="15m",
)

crfs_18m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=220, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="18m",
)

crfs_21m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="21m",
)

crfs_24m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.glucose"),
    Crf(show_order=210, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=220, model="meta_subject.bloodresultsrft"),
    Crf(show_order=230, model="meta_subject.bloodresultslft"),
    Crf(show_order=240, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=250, model="meta_subject.bloodresultslipid"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="24m",
)

crfs_27m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="27m",
)

crfs_30m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=210, model="meta_subject.bloodresultsrft"),
    Crf(show_order=220, model="meta_subject.bloodresultslft"),
    Crf(show_order=230, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="30m",
)

crfs_33m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="33m",
)

crfs_36m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followupexamination"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    Crf(show_order=210, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=220, model="meta_subject.bloodresultsrft"),
    Crf(show_order=230, model="meta_subject.bloodresultslft"),
    Crf(show_order=240, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=250, model="meta_subject.bloodresultslipid"),
    Crf(show_order=300, model="meta_subject.studydrugrefill"),
    Crf(show_order=310, model="meta_subject.medicationadherence"),
    name="36m",
)
