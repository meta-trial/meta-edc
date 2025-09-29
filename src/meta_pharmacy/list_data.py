from edc_sites.site import sites as site_sites

list_data = {
    "edc_pharmacy.location": [
        ("central", "Central"),
        *[(ss.name, ss.description) for ss in site_sites.all(aslist=True)],
    ],
}
