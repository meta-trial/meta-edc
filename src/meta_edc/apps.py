from django.apps import AppConfig as DjangoAppConfig
from django.contrib.admin.apps import AdminConfig as DjangoAdminConfig
from django.core.management.color import color_style

from meta_edc.meta_version import get_meta_version

style = color_style()


class AdminConfig(DjangoAdminConfig):
    default_site = "meta_edc.admin.AdminSite"


class AppConfig(DjangoAppConfig):
    name = "meta_edc"
    verbose_name = f"META Phase {get_meta_version()}"
