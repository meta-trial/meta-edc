from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = "Meta Export"
    site_header = "Meta Export"
    index_title = "Meta Export"
    site_url = "/administration/"


meta_export_admin = AdminSite(name="meta_export_admin")
