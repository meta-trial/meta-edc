from django.apps import AppConfig as DjangoAppConfig

from meta_edc.meta_version import get_meta_version


class AppConfig(DjangoAppConfig):
    name = "meta_export"
    verbose_name = f"META{get_meta_version()}: Export Data"
