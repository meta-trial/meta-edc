Changes
=======

0.1.77 - 0.1.79
---------------
- add pregnancy, delivery, birth outcomes
- add repeat glucose tests in screening part three
- BMI normal range (5-60)
- remove all conditional statements for PHASE2
- remove sarscov2 requirement
- remove PHASE2 randomizer
- remove PHAS2 only tests
- add part three report datetime to form
- change fasting blood glucose field prefix from `ifg` to `fbg`
- add <400 in last 6m question to P3 screening
- add migrations

0.1.76
------
- set week 2 lower bound to 3 days in window period
- rename euro-qol auth groups in auths.py
- rename rando groups in auths.py
- add meta_pharmacy app
- missing prescriptions management command
- add StudyMedicationForm
- create prescription in signal on consent post-save
- update offstudy reasons in list_data.py
- populate static pharmacy models in signal (apps.py)
- separate admin class for Phase 3 EoS
- update phase 3 withdrawal reasons (meta_prn.choices.py)
- add EndOfStudyPhaseThreeForm, EndOfStudyPhaseThreeFormValidator
- add last_seen_date, clinical_withdrawal_reason,
  toxicity_withdrawal_reason to EoS model
- refactor eligibility classes - part 1,2,3
- add fasting_opinion question to glucose
- PartFourFieldsModelMixin
- ask "Was the subject enrolled in the META Phase 2 trial?" (part_one_fields_model_mixin.py)
- remove oxygen_saturation
- import from edc_qol
- add to patient history: previous_arv_regimen_start_date
- fix pdf report - point to FollowupVitals.weight (meta_reports)

0.1.75
------
- bump edc to 0.3.50
- add euro-qol eq5d3l at 2 week visit
- empty models for study medication and concomitant medication

0.1.74
------
- bump up edc to 0.3.49

0.1.73
------
- bump up edc to 0.3.46

0.1.71
------
- update auths for changes in edc-auth 

0.1.70
------
- separate Phase 2 and Phase 3 screening: inclusion
  criteria, randomizer, table, etc (meta_screening)
- add table randomizationlist (accessible in Phase 3) (meta_rando)
- rename fields in model SubjectScreening` -- `stay_nearby`
  to `stay_nearby_6` (meta_screening)
- add fields to model SubjectScreening -- `has_dm`, `on_dm_medication`, `severe_htn`
  (accessible in Phase 3) (meta_screening)
- add fields to model SubjectScreening for BP 2X readings/avg
  (accessible in Phase 3) (meta_screening)
- add separate Phase 3 visit schedule / data collection schedule
  (meta_visit_schedule)
- add bloodresult utest_ids for MCH, MCHC, MCV. Migrate fields
  into existing BloodResultsFbc (meta_subject)
- add bloodresult utestids for CHOL. Migrate fields
  into existing BloodResultsLipids (meta_subject)
- add HepatitisTest model, add dyslipidaemia_rx to PatientHistory
  model (accessible in Phase 3) (meta_subject)
- require `edc_vitals` for field classes used in models PhysicalExam
  and FollowupVitals (meta_subject)
- add model StudyDrugRefill, AdditionalScreening
  (accessible in Phase 3) (meta_subject)
- add ComplicationsGlycemia (accessible for Phase 3 / pending)
  (meta_subject)
- require `edc-mnsi`. MNSI /  (accessible in Phase 3) (meta_subject)
- add OtherArvRegimens model (accessible in Phase 3) (meta_subject)
- add nullable fields to PatientHistory:
  concomitant_medications, other_dyslipidaemia_rx
  (accessible in Phase 3) (meta_subject)
- add inline model OtherArvRegimensDetail to capture history of ARVs
  (accessible in Phase 3) (meta_subject)
- add fields to model FollowupVitals for BP 2X readings/avg
  (accessible in Phase 3) (meta_subject)
- leave 1X BP reading fields in FollowupVitals for Phase 2, make
  nullable but required if in Admin (meta_subject)
- create model BloodResultsIns (accessible in Phase 3) (meta_subject)
- rename fields in model PatientHistory (0075):
  diabetes_in_family->dm_in_family
  diabetes_symptoms->dm_symptoms
  hypertension_treatment->htn_treatment
  on_hypertension_treatment->on_htn_treatment
  other_diabetes_symptoms->other_dm_symptoms
  other_hypertension_treatment->other_htn_treatment
  (meta_subject)
- add model HealthEconomicsSimple. Require on or after W2
  (accessible in Phase 3) (meta_subject)
- move Unblinding models from meta_prn to edc_unblinding (meta_prn)
- rename field in model ProtocolDeviationViolation `violation_type` to `violation`.
  Also change datatype from CharField to ForeignKey. Update data to match existing.
  (meta_prn)
- rename field in model ProtocolDeviationViolation `violation_type_other`
  to `violation_other` (meta_prn)
- Change datatype of field in model ProtocolDeviationViolation `actions_required`
  from CharField to ForeignKey. Update data to match existing (meta_prn)

0.1.66
------
- see docs for details of field name changes: docs/updates/1.65/renamed_fields.txt

0.1.63
------
- evaluate glucose field values consistently in form validators
- change fasted to fasting for consistency
- update lab / utestid field to have "_value" suffix
- update imports for classes moved out of respond africa

0.1.60
------
- rename model ``Follow`` to ``FollowupExamination``
- add HIV regimen to ``FollowupExamination`` in HIV section
- improve validation for ``FollowupExamination``: ensure lists of G3/G4 symptoms do not overlap and are from the original list of symptoms; other minor validation checks.
- add action to Followup Examination to notify of AE
- update missed visit; rename to Subject Visit Missed and keep related list model in ``meta_lists``
- change to LOST_TO_FOLLOWUP in lists, update existing instances
- fix HbA1c form validation / grading
- upgrade to edc==0.1.32

0.1.57
------
- add Glucose (IFG, OGTT) CRF to 6m, 12m
- add missed visit CRF
- upgrade to edc==0.1.29

0.1.56
------
- add sarscov2 permissions to CLINIC

0.1.56
------
- sarscov2==0.1.9

0.1.55
------
- add KAP links from subject listboard
- use ``?next=`` querystring attr on KAP link

0.1.54
------
- add hba1c, glu, fbc, lipids, etc to 6m
- upgrade to edc==0.1.28

0.1.52
------
- upgrade to edc==0.1.27
- remove KAP model, add back with sarscov2 reuseable app
- add links from screening listboard
- meta_ae app is in progress

0.1.51
------
- add Corona virus KAP form to DAY1 and as a PRN for those past DAY1

0.1.50
------
- add Uganda hosts to ``nginx.conf`` and ``ALLOWED_HOSTS``
- bump up edc==0.1.18

0.1.46
------
- bump up to DJ>=3.0.3, python 3.8, edc==0.1.10

