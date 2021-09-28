from edc_lab_panel.panels import hba1c_poc_panel
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import (
    CrfRule,
    CrfRuleGroup,
    P,
    RequisitionRule,
    RequisitionRuleGroup,
    register,
)

from .predicates import Predicates

pc = Predicates()


@register()
class HealthEconomicsRuleGroup(CrfRuleGroup):

    hecon = CrfRule(
        predicate=pc.health_economics_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["healtheconomicssimple"],
    )

    class Meta:
        app_label = "meta_subject"
        source_model = "meta_subject.subjectvisit"


@register()
class HepatitisTestRuleGroup(CrfRuleGroup):

    hep = CrfRule(
        predicate=pc.hepatitis_test_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hepatitistest"],
    )

    class Meta:
        app_label = "meta_subject"
        source_model = "meta_subject.subjectvisit"


@register()
class HbA1cCrfRuleGroup(CrfRuleGroup):

    hba1c = CrfRule(
        predicate=pc.hba1c_crf_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["bloodresultshba1c"],
    )

    class Meta:
        app_label = "meta_subject"
        source_model = "meta_subject.subjectvisit"


@register()
class HbA1cRequisitionRuleGroup(RequisitionRuleGroup):

    hba1c = RequisitionRule(
        predicate=pc.hba1c_requisition_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[hba1c_poc_panel],
    )

    class Meta:
        app_label = "meta_subject"
        source_model = "meta_subject.subjectvisit"
        requisition_model = "meta_subject.subjectrequisition"
