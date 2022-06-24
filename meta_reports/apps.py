from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig

from meta_edc.meta_version import get_meta_version


class AppConfig(DjangoAppConfig):
    name = "meta_reports"
    verbose_name = f"META{get_meta_version()}: Reports"


if settings.APP_NAME == "meta_reports":

    from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE

    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = "tanzania"
        definitions = {
            "7-day-clinic": dict(
                days=[MO, TU, WE, TH, FR, SA, SU],
                slots=[100, 100, 100, 100, 100, 100, 100],
            ),
            "5-day-clinic": dict(days=[MO, TU, WE, TH, FR], slots=[100, 100, 100, 100, 100]),
        }
