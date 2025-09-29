from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "meta_rando"
    verbose_name = "META Randomization"
    include_in_administration_section = False
    default_auto_field = "django.db.models.BigAutoField"
