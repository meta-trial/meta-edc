from django.apps import AppConfig as DjangoAppConfig
from django.db.models.signals import post_migrate
from django_extensions.management.color import color_style

from meta_edc.meta_version import get_meta_version

from .prepare_meta_pharmacy import prepare_meta_pharmacy

style = color_style()


def post_migrate_populate_pharmacy_models(sender=None, **kwargs):  # noqa
    """Create or update pharmacy static models."""
    prepare_meta_pharmacy()


class AppConfig(DjangoAppConfig):
    name = "meta_pharmacy"
    verbose_name = f"META{get_meta_version()}: Pharmacy"

    def ready(self):
        post_migrate.connect(post_migrate_populate_pharmacy_models, sender=self)
