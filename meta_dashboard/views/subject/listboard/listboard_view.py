import re
from typing import List

from django.db.models import Q
from edc_listboard.views import SubjectListboardView as BaseSubjectListboardView

from meta_edc.meta_version import get_meta_version


class SubjectListboardView(BaseSubjectListboardView):
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update(meta_version=get_meta_version())
        return context

    def extra_search_options(self, search_term) -> List[Q]:
        q_objects = super().extra_search_options(search_term)
        if re.match(r"^[0-9\-]+$", search_term):
            q_objects.append(Q(identity__exact=search_term))
        return q_objects
