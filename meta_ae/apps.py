from django.apps import AppConfig as DjangoAppConfig

from meta_edc.meta_version import get_meta_version


class AppConfig(DjangoAppConfig):
    name = "meta_ae"
    verbose_name = f"META{get_meta_version()}: Adverse Events"
    include_in_administration_section = True
    has_exportable_data = True
    default_auto_field = "django.db.models.BigAutoField"
