from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_reportable.constants import GRADE4
from edc_utils.date import get_utcnow
from model_bakery.recipe import Recipe

from meta_ae.models.ae_followup import AeFollowup
from meta_ae.models.ae_initial import AeInitial
from meta_ae.models.ae_susar import AeSusar
from meta_ae.models.ae_tmg import AeTmg
from meta_ae.models.death_report import DeathReport

aeinitial = Recipe(
    AeInitial,
    action_identifier=None,
    tracking_identifier=None,
    ae_description="A description of this event",
    ae_grade=GRADE4,
    ae_study_relation_possibility=YES,
    ae_start_date=get_utcnow().date(),
    ae_awareness_date=get_utcnow().date(),
    study_drug_relation="not_related",
    ae_treatment="Some special treatment",
    sae=NO,
    susar=NO,
    susar_reported=NOT_APPLICABLE,
    ae_cause=NO,
    ae_cause_other=None,
)

aetmg = Recipe(AeTmg, action_identifier=None, tracking_identifier=None)

aesusar = Recipe(AeSusar, action_identifier=None, tracking_identifier=None)

aefollowup = Recipe(
    AeFollowup, relevant_history=NO, action_identifier=None, tracking_identifier=None
)

deathreport = Recipe(
    DeathReport,
    subject_identifier=None,
    action_identifier=None,
    tracking_identifier=None,
)
