from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "meta_visit_schedule"
    verbose_name = "META: Visit Schedule"
