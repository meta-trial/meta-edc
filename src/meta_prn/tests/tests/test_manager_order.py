from django.apps import apps as django_apps
from django.test import override_settings, TestCase
from edc_sites.managers import CurrentSiteManager


@override_settings(SITE_ID=10)
class TestManagers(TestCase):
    def test_models(self):
        app_config = django_apps.get_app_config("meta_prn")
        for model_cls in app_config.get_models():
            if "historical" not in model_cls._meta.label_lower:
                self.assertFalse(
                    isinstance(model_cls._default_manager, (CurrentSiteManager,)),
                    msg=model_cls._meta.label_lower,
                )
