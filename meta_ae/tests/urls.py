from meta_ae.admin_site import meta_ae_admin
from django.contrib import admin
from django.urls.conf import path, include

urlpatterns = [
    path("ae/", include("meta_ae.urls")),
    path("admin/", meta_ae_admin.urls),
    path("admin/", admin.site.urls),
]
