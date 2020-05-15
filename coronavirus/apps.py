from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = "coronavirus"
    verbose_name = "Coronavirus"
    include_in_administration_section = True
    has_exportable_data = True
