from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import CrfRule, CrfRuleGroup, P, register

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
class HbA1cTestRuleGroup(CrfRuleGroup):

    hba1c = CrfRule(
        predicate=pc.hba1c_required_at_baseline,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["bloodresultshba1c"],
    )

    class Meta:
        app_label = "meta_subject"
        source_model = "meta_subject.subjectvisit"
