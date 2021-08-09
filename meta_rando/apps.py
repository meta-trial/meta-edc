from django.apps import AppConfig as DjangoAppConfig

from meta_edc.meta_version import get_meta_version


class AppConfig(DjangoAppConfig):
    name = "meta_rando"
    verbose_name = f"META{get_meta_version()}: Randomization"
    include_in_administration_section = False
    default_auto_field = "django.db.models.BigAutoField"
