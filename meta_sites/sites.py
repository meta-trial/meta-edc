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
            domain=f"hindu-mandal.tz.{fqdn}",
        ),
        SingleSite(
            20,
            "amana",
            title="Amana Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"amana.tz.{fqdn}",
        ),
        SingleSite(
            30,
            "temeke",
            title="Temeke Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"temeke.tz.{fqdn}",
        ),
    ),
}
