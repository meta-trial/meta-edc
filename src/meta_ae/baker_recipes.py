from clinicedc_constants import GRADE4, NO, NOT_APPLICABLE, NOT_RELATED, YES
from django.utils import timezone
from model_bakery.recipe import Recipe

from meta_ae.models.ae_followup import AeFollowup
from meta_ae.models.ae_initial import AeInitial
from meta_ae.models.ae_susar import AeSusar
from meta_ae.models.ae_tmg import AeTmg
from meta_ae.models.death_report import DeathReport

aeinitial = Recipe(
    AeInitial,
    action_identifier=None,
    ae_description="A description of this event",
    ae_grade=GRADE4,
    ae_study_relation_possibility=YES,
    ae_start_date=timezone.now().date(),
    ae_awareness_date=timezone.now().date(),
    study_drug_relation=NOT_RELATED,
    ae_treatment="Some special treatment",
    sae=NO,
    susar=NO,
    susar_reported=NOT_APPLICABLE,
    ae_cause=NO,
    ae_cause_other=None,
)

aetmg = Recipe(AeTmg, action_identifier=None)

aesusar = Recipe(AeSusar, action_identifier=None)

aefollowup = Recipe(AeFollowup, relevant_history=NO, action_identifier=None)

deathreport = Recipe(
    DeathReport,
    subject_identifier=None,
    action_identifier=None,
)
