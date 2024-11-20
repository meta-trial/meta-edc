from django.apps import AppConfig as DjangoAppConfig
from django.db.models.signals import post_migrate
from django_extensions.management.color import color_style
from edc_list_data import site_list_data

from .prepare_meta_pharmacy import prepare_meta_pharmacy

style = color_style()


def post_migrate_populate_pharmacy_models(sender=None, **kwargs):  # noqa
    """Create or update pharmacy static models."""
    site_list_data.load_data()
    prepare_meta_pharmacy()


class AppConfig(DjangoAppConfig):
    name = "meta_pharmacy"
    verbose_name = "META Pharmacy"
    include_in_administration_section = True
    has_exportable_data = True
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        post_migrate.connect(post_migrate_populate_pharmacy_models, sender=self)
