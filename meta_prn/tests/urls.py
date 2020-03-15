from meta_prn.admin_site import meta_prn_admin
from django.contrib import admin
from django.urls.conf import path, include

urlpatterns = [
    path("meta_prn/", include("meta_prn.urls")),
    path("admin/", meta_prn_admin.urls),
    path("admin/", admin.site.urls),
]
