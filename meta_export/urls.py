from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import meta_export_admin

app_name = "meta_export"

urlpatterns = [
    path("admin/", meta_export_admin.urls),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]
