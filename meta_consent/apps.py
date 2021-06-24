from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "meta_consent"
    verbose_name = "META: Consent"
    include_in_administration_section = True
    has_exportable_data = True
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from .models.signals import subject_consent_on_post_delete  # noqa
        from .models.signals import subject_consent_on_post_save  # noqa; noqa
