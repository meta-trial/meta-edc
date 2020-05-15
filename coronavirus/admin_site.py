from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = "Coronavirus"
    site_header = "Coronavirus"
    index_title = "Coronavirus"
    site_url = "/administration/"


coronavirus_admin = AdminSite(name="coronavirus_admin")
coronavirus_admin.disable_action("delete_selected")
