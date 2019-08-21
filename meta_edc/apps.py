import sys

from django.conf import settings
from meta_sites import meta_sites, fqdn
from datetime import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps
from django.core.checks import register
from django.core.management.color import color_style
from django.db.models.signals import post_migrate
# from django_collect_offline.apps import AppConfig as BaseDjangoCollectOfflineAppConfig
from edc_appointment.appointment_config import AppointmentConfig
from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig

# from .system_checks import meta_check


style = color_style()


def post_migrate_update_sites(sender=None, **kwargs):
    from edc_sites.utils import add_or_update_django_sites

    sys.stdout.write(style.MIGRATE_HEADING("Updating sites:\n"))
    add_or_update_django_sites(
        apps=django_apps, sites=meta_sites, fqdn=fqdn, verbose=True
    )
    sys.stdout.write("Done.\n")
    sys.stdout.flush()


def post_migrate_update_edc_permissions(sender=None, **kwargs):
    from meta_permissions.updaters import update_permissions

    sys.stdout.write(style.MIGRATE_HEADING("Updating permissions:\n"))
    update_permissions()
    sys.stdout.write("Done.\n")
    sys.stdout.flush()


class AppConfig(DjangoAppConfig):
    name = 'meta_edc'

    def ready(self):
        from meta_rando.system_checks import randomization_list_check

        register(randomization_list_check)(["meta_edc"])
        # register(meta_check)
        post_migrate.connect(post_migrate_update_sites, sender=self)
        post_migrate.connect(post_migrate_update_edc_permissions, sender=self)


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    institution = "LIverpool School ofTropical Medicine"
    project_name = "META"
    project_repo = "https://github.com/meta-trail"
    protocol = "LSTM001"
    protocol_name = "META"
    protocol_number = "101"
    protocol_title = (
        "META Trial"
    )
    study_open_datetime = datetime(2019, 7, 31, 0, 0, 0, tzinfo=gettz("UTC"))
    study_close_datetime = datetime(
        2022, 12, 31, 23, 59, 59, tzinfo=gettz("UTC"))


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    device_role = CENTRAL_SERVER
    device_id = "99"


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        "meta_subject": ("subject_visit", "meta_subject.subjectvisit")
    }


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = "101"


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {"meta_subject.subjectvisit": "reason"}


class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
    configurations = [
        AppointmentConfig(
            model="edc_appointment.appointment",
            related_visit_model="meta_subject.subjectvisit",
            appt_type="hospital",
        )
    ]


class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
    country = settings.COUNTRY
    definitions = {
        "7-day clinic": dict(
            days=[MO, TU, WE, TH, FR, SA, SU], slots=[
                100, 100, 100, 100, 100, 100, 100]
        ),
        "5-day clinic": dict(
            days=[MO, TU, WE, TH, FR], slots=[100, 100, 100, 100, 100]
        ),
    }


# class DjangoCollectOfflineAppConfig(BaseDjangoCollectOfflineAppConfig):
#     base_template_name = "edc_dashboard/bootstrap3/base.html"
