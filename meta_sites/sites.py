from edc_sites.single_site import SingleSite

fqdn = "meta3.clinicedc.org"


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
        SingleSite(
            40,
            "mwananyamala",
            title="Mwananyamala Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"mwananyamala.tz.{fqdn}",
        ),
        SingleSite(
            50,
            "mbagala",
            title="Mbagala Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"mbagala.tz.{fqdn}",
        ),
        SingleSite(
            60,
            "mnazi_moja",
            title="Mnazi Moja Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"mnazi-moja.tz.{fqdn}",
        ),
    ),
}
