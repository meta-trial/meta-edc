from django.conf import settings
from edc_sites.single_site import SingleSite
from edc_sites.site import sites as site_sites

domain_suffix = settings.EDC_SITES_DOMAIN_SUFFIX
languages = ["sw", "en", "mas"]

all_sites = [
    SingleSite(
        10,
        "hindu_mandal",
        title="Hindu Mandal Hospital",
        country="tanzania",
        country_code="tz",
        domain=f"hindu-mandal.tz.{domain_suffix}",
        language_codes=languages,
    ),
    SingleSite(
        20,
        "amana",
        title="Amana Hospital",
        country="tanzania",
        country_code="tz",
        domain=f"amana.tz.{domain_suffix}",
        language_codes=languages,
    ),
    SingleSite(
        30,
        "temeke",
        title="Temeke Hospital",
        country="tanzania",
        country_code="tz",
        domain=f"temeke.tz.{domain_suffix}",
        language_codes=languages,
    ),
    SingleSite(
        40,
        "mwananyamala",
        title="Mwananyamala Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=languages,
        domain=f"mwananyamala.tz.{domain_suffix}",
    ),
    SingleSite(
        50,
        "mbagala",
        title="Mbagala Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=languages,
        domain=f"mbagala.tz.{domain_suffix}",
    ),
    SingleSite(
        60,
        "mnazi_moja",
        title="Mnazi Moja Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=languages,
        domain=f"mnazi-moja.tz.{domain_suffix}",
    ),
]

site_sites.register(*all_sites)
