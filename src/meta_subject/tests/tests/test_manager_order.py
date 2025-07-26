from django.apps import apps as django_apps
from django.test import TestCase
from edc_sites.managers import CurrentSiteManager


class TestManagers(TestCase):
    def test_default_model_manager_not_site_manager(self):
        app_label = "meta_subject"
        app_config = django_apps.get_app_config(app_label)
        for model_cls in app_config.get_models():
            self.assertFalse(isinstance(model_cls._default_manager, (CurrentSiteManager,)))
