from copy import copy
from django.conf import settings
from edc_lab_dashboard.navbars import navbar as lab_navbar
from edc_navbar import site_navbars, Navbar
from edc_review_dashboard.navbars import navbar as review_navbar
from meta_dashboard.navbars import navbar as meta_dashboard_navbar

navbar = Navbar(name=settings.APP_NAME)

navbar_item = copy([item for item in lab_navbar.items if item.name == "specimens"][0])
navbar_item.active = False
navbar_item.label = "Specimens"
navbar.append_item(navbar_item)

navbar.append_item(
    [item for item in meta_dashboard_navbar.items if item.name == "screened_subject"][0]
)

navbar.append_item(
    [item for item in meta_dashboard_navbar.items if item.name == "consented_subject"][
        0
    ]
)

for item in review_navbar.items:
    navbar.append_item(item)

navbar.append_item(
    [item for item in meta_dashboard_navbar.items if item.name == "ae_home"][0]
)

navbar.append_item(
    [item for item in meta_dashboard_navbar.items if item.name == "data_manager_home"][
        0
    ]
)

site_navbars.register(navbar)
