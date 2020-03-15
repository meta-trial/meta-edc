from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import meta_lists_admin

app_name = "meta_lists"

urlpatterns = [
    path("admin/", meta_lists_admin.urls),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]
