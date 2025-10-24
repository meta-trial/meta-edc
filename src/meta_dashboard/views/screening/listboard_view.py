from edc_listboard.views import ScreeningListboardView

from meta_edc.meta_version import get_meta_version


class ListboardView(ScreeningListboardView):
    listboard_model = "meta_screening.screeningpartone"
    navbar_selected_item = "screened_subject"

    def get_context_data(self, **kwargs) -> dict:
        kwargs.update(meta_version=get_meta_version())
        return super().get_context_data(**kwargs)

    def get_search_fields(self) -> tuple[str, ...]:
        fields = super().get_search_fields()
        return *fields, "hospital_identifier__exact"
