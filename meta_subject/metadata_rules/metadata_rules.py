from edc_lab_panel.panels import hba1c_poc_panel, insulin_panel
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import (
    CrfRule,
    CrfRuleGroup,
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


@register()
class InsulinCrfRuleGroup(CrfRuleGroup):

    insulin = CrfRule(
        predicate=pc.insulin_crf_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["bloodresultsins"],
    )

    class Meta:
        app_label = "meta_subject"
        source_model = "meta_subject.subjectvisit"


@register()
class InsulinRequisitionRuleGroup(RequisitionRuleGroup):

    insulin = RequisitionRule(
        predicate=pc.insulin_requisition_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[insulin_panel],
    )

    class Meta:
        app_label = "meta_subject"
        source_model = "meta_subject.subjectvisit"
        requisition_model = "meta_subject.subjectrequisition"


@register()
class MnsiTestRuleGroup(CrfRuleGroup):

    mnsi = CrfRule(
        predicate=pc.mnsi_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["mnsi"],
    )

    class Meta:
        app_label = "meta_subject"
        source_model = "meta_subject.subjectvisit"


@register()
class Sf12RuleGroup(CrfRuleGroup):

    sf12 = CrfRule(
        predicate=pc.sf12_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["sf12"],
    )

    class Meta:
        app_label = "meta_subject"
        source_model = "meta_subject.subjectvisit"


@register()
class Eq53dlRuleGroup(CrfRuleGroup):

    eq5d3l = CrfRule(
        predicate=pc.eq5d3l_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["eq5d3l"],
    )

    class Meta:
        app_label = "meta_subject"
        source_model = "meta_subject.subjectvisit"
