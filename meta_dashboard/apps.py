from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from datetime import datetime
from dateutil.tz.tz import gettz


class AppConfig(DjangoAppConfig):
    name = "meta_dashboard"
    admin_site_name = "meta_test_admin"
    include_in_administration_section = False


if settings.APP_NAME == "meta_dashboard":
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
    from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig

    class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
        protocol = "EDC092"
        protocol_name = "META"
        protocol_number = "092"
        protocol_title = ""
        study_open_datetime = datetime(2019, 7, 31, 0, 0, 0, tzinfo=gettz("UTC"))
        study_close_datetime = datetime(2022, 12, 31, 23, 59, 59, tzinfo=gettz("UTC"))

    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = "tanzania"
        definitions = {
            "7-day-clinic": dict(
                days=[MO, TU, WE, TH, FR, SA, SU],
                slots=[100, 100, 100, 100, 100, 100, 100],
            ),
            "5-day-clinic": dict(
                days=[MO, TU, WE, TH, FR], slots=[100, 100, 100, 100, 100]
            ),
        }

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {"meta_subject": ("subject_visit", "meta_subject.subjectvisit")}

    class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
        identifier_prefix = "092"

    class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
        reason_field = {"meta_subject.subjectvisit": "reason"}
