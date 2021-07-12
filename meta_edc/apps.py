from django.apps import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps
from django.core.management.color import color_style
from django.db.models.signals import post_migrate
from edc_auth.group_permissions_updater import GroupPermissionsUpdater

style = color_style()


def post_migrate_update_edc_auth(sender=None, **kwargs):
    from meta_auth.codenames_by_group import get_codenames_by_group

    GroupPermissionsUpdater(
        codenames_by_group=get_codenames_by_group(), verbose=True, apps=django_apps
    )


class AppConfig(DjangoAppConfig):
    name = "meta_edc"

    def ready(self):
        post_migrate.connect(post_migrate_update_edc_auth, sender=self)
