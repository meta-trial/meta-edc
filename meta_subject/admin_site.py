from django.contrib.admin import AdminSite as DjangoAdminSite
from django.contrib.sites.shortcuts import get_current_site
from edc_sites.models import SiteProfile


class AdminSite(DjangoAdminSite):

    site_title = "META Subject CRFs"
    site_header = "META Subject CRFs"
    index_title = "META Subject CRFs"
    site_url = "/administration/"

    def each_context(self, request):
        context = super().each_context(request)
        title = SiteProfile.objects.get(site=get_current_site(request)).title
        context.update(global_site=get_current_site(request))
        label = f"META: {title.title()} - Subject CRFs"
        context.update(site_title=label, site_header=label, index_title=label)
        return context


meta_subject_admin = AdminSite(name="meta_subject_admin")
meta_subject_admin.disable_action("delete_selected")
