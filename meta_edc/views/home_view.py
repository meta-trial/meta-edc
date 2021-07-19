from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin
from edc_randomization.site_randomizers import site_randomizers

from meta_edc.meta_version import get_meta_version


class HomeView(EdcViewMixin, NavbarViewMixin, TemplateView):

    template_name = f"meta_edc/bootstrap{settings.EDC_BOOTSTRAP}/home.html"
    navbar_name = settings.APP_NAME
    navbar_selected_item = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        randomizer_cls = site_randomizers.get(get_meta_version())
        edc_randomization_url = reverse(
            f"edc_randomization_admin:{randomizer_cls.model_cls()._meta.label_lower.replace('.', '_')}_changelist"
        )
        context.update(edc_randomization_url=edc_randomization_url)
        return context
