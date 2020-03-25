from edc_sites.single_site import SingleSite

fqdn = "meta.clinicedc.org"

all_sites = {
    "tanzania": (
        SingleSite(
            10,
            "hindu_mandal",
            title="Hindu Mandal Hospital",
            country="tanzania",
            country_code="tz",
            fqdn=fqdn,
        ),
        SingleSite(
            20,
            "amana",
            title="Amana Hospital",
            country="tanzania",
            country_code="tz",
            fqdn=fqdn,
        ),
        SingleSite(
            30,
            "temeke",
            title="Temeke Hospital",
            country="tanzania",
            country_code="tz",
            fqdn=fqdn,
        ),
    ),
}
