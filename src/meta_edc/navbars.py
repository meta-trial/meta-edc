from copy import copy

from django.conf import settings
from edc_adverse_event.navbars import ae_navbar_item, tmg_navbar_item
from edc_data_manager.navbar_item import dm_navbar_item
from edc_lab_dashboard.navbars import navbar as lab_navbar
from edc_navbar import Navbar, site_navbars
from edc_pharmacy.navbars import pharmacy_navbar_item
from edc_review_dashboard.navbars import navbar as review_navbar

from meta_dashboard.navbars import navbar as meta_dashboard_navbar

navbar = Navbar(name=settings.APP_NAME)

navbar_item = copy(next(item for item in lab_navbar.navbar_items if item.name == "specimens"))
navbar_item.active = False
navbar_item.label = "Specimens"
navbar.register(navbar_item)

navbar.register(
    next(
        item for item in meta_dashboard_navbar.navbar_items if item.name == "screened_subject"
    )
)

navbar.register(
    next(
        item for item in meta_dashboard_navbar.navbar_items if item.name == "consented_subject"
    )
)

for navbar_item in review_navbar.navbar_items:
    navbar.register(navbar_item)

navbar.register(pharmacy_navbar_item)
navbar.register(tmg_navbar_item)
navbar.register(ae_navbar_item)
navbar.register(dm_navbar_item)

site_navbars.register(navbar)
