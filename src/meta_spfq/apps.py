from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style
from django.db.models.signals import post_migrate

from meta_spfq.utils import import_spfq_list

style = color_style()


def update_spfq_list_on_post_migrate(sender, **kwargs):  # noqa: ARG001
    import_spfq_list()


class AppConfig(DjangoAppConfig):
    name = "meta_spfq"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "META Feedback (SPFQ)"
    include_in_administration_section = True
    has_exportable_data = True

    def ready(self):
        post_migrate.connect(
            update_spfq_list_on_post_migrate,
            sender=self,
            dispatch_uid="meta_spfq.update_spfq_list_on_post_migrate",
        )
