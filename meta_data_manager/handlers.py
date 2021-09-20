from django.core.exceptions import ObjectDoesNotExist
from edc_data_manager.handlers import QueryRuleHandler

from meta_screening.models import SubjectScreening


class BaselineHbA1cRuleHandler(QueryRuleHandler):

    name = "baseline_hba1c"
    display_name = "Baseline HbA1c"
    model_name = "meta_subject.bloodresultshba1c"

    def run(self):
        try:
            SubjectScreening.objects.get(
                subject_identifier=self.visit_obj.subject_identifier,
                hba1c_value__isnull=False,
            )
        except ObjectDoesNotExist:
            if self.resolved:
                self.data_query = self.get_or_create_data_query(get_only=True)
                if self.data_query:
                    self.resolve_existing_data_query()
            else:
                self.data_query = self.get_or_create_data_query()
                if self.data_query.site_resolved:
                    self.reopen_existing_data_query()
