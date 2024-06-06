from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "meta_reports"
    verbose_name = "META Reports"
    include_in_administration_section = True
