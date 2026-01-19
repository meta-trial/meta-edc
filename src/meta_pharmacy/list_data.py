from edc_pharmacy.constants import CENTRAL_LOCATION
from edc_sites.site import sites as site_sites

list_data = {
    "edc_pharmacy.location": [
        (CENTRAL_LOCATION, "Central"),
        *[(ss.name, ss.description) for ss in site_sites.all(aslist=True)],
    ],
}
