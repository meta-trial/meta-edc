from django.apps import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps
from django.core.checks import register
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

        # from edc_randomization.system_checks import randomization_list_check
        #
        # register(randomization_list_check)(["meta_edc"])
        # register(meta_check)


# class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
#     institution = "Liverpool School of Tropical Medicine (LSTM)"
#     project_name = "META"
#     project_repo = "https://github.com/meta-trail"
#     protocol = "META"
#     protocol_name = "META"
#     protocol_number = "101"
#     protocol_title = "META Trial"
#     study_open_datetime = datetime(2019, 7, 31, 0, 0, 0, tzinfo=gettz("UTC"))
#     study_close_datetime = datetime(2022, 12, 31, 23, 59, 59, tzinfo=gettz("UTC"))
