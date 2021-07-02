Changes
=======

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

