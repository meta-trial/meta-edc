from edc_listboard.views import SubjectListboardView as BaseSubjectListboardView

from meta_edc.meta_version import get_meta_version


class SubjectListboardView(BaseSubjectListboardView):
    listboard_model = "meta_consent.subjectconsent"
    navbar_selected_item = "consented_subject"

    def get_context_data(self, **kwargs) -> dict:
        kwargs.update(meta_version=get_meta_version())
        return super().get_context_data(**kwargs)

    def get_search_fields(self) -> list[str]:
        fields = super().get_search_fields()
        fields.append("identity__exact")
        return fields
