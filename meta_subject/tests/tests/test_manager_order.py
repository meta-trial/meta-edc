from django.apps import apps as django_apps
from django.test import TestCase
from edc_sites.models import CurrentSiteManager as DefaultCurrentSiteManager
from edc_visit_tracking.managers import CrfCurrentSiteManager, VisitCurrentSiteManager


class TestManagers(TestCase):
    def test_models(self):
        app_label = "meta_subject"
        app_config = django_apps.get_app_config(app_label)
        inlines = [f"{app_label}.birthoutcomes", f"{app_label}.otherarvregimensdetail"]
        visit_model = f"{app_label}.subjectvisit"
        for model_cls in app_config.get_models():
            if model_cls._meta.label_lower in inlines:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    DefaultCurrentSiteManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower == visit_model:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    VisitCurrentSiteManager,
                    msg=f"Model is {model_cls}",
                )
            elif "historical" not in model_cls._meta.label_lower:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    CrfCurrentSiteManager,
                    msg=f"Model is {model_cls}",
                )
