from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = "meta_auth"
    verbose_name = "Meta Authentication and Permissions"
