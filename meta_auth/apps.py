from django.apps import AppConfig as DjangoApponfig

from meta_edc.meta_version import get_meta_version


class AppConfig(DjangoApponfig):
    name = "meta_auth"
    verbose_name = f"META{get_meta_version()}: Authentication and Permissions"
    default_auto_field = "django.db.models.BigAutoField"
