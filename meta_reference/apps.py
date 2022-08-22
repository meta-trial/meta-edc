from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "meta_reference"
    verbose_name = "META Reference"
