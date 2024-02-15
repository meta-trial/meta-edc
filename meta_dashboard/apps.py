from django.apps import AppConfig as DjangoAppConfig

from meta_edc.meta_version import get_meta_version


class AppConfig(DjangoAppConfig):
    name = "meta_dashboard"
    verbose_name = f"META{get_meta_version()}: Dashboard"
    admin_site_name = "meta_test_admin"
    include_in_administration_section = False
