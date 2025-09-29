from django.contrib import admin
from django.urls.conf import include, path

from meta_prn.admin_site import meta_prn_admin

urlpatterns = [
    path("meta_prn/", include("meta_prn.urls")),
    path("admin/", meta_prn_admin.urls),
    path("admin/", admin.site.urls),
]
