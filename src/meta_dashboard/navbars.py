from edc_adverse_event.navbars import ae_navbar_item, tmg_navbar_item
from edc_data_manager.navbar_item import dm_navbar_item
from edc_navbar import Navbar, NavbarItem, site_navbars
from edc_pharmacy.navbars import pharmacy_navbar_item
from edc_review_dashboard.navbars import navbar_item as review_navbar_item

no_url_namespace = False  # True if settings.APP_NAME == "meta_dashboard" else False

navbar = Navbar(name="meta_dashboard")


navbar.register(
    NavbarItem(
        name="screened_subject",
        title="Screening",
        label="Screening",
        fa_icon="fa-user-plus",
        codename="edc_screening.view_screening_listboard",
        url_name="screening_listboard_url",
        no_url_namespace=no_url_namespace,
    )
)

navbar.register(
    NavbarItem(
        name="consented_subject",
        title="Subjects",
        label="Subjects",
        fa_icon="fa-user-circle",
        codename="edc_subject_dashboard.view_subject_listboard",
        url_name="subject_listboard_url",
        no_url_namespace=no_url_namespace,
    )
)


navbar.register(pharmacy_navbar_item)
navbar.register(review_navbar_item)
navbar.register(tmg_navbar_item)
navbar.register(ae_navbar_item)
navbar.register(dm_navbar_item)
site_navbars.register(navbar)
