from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import meta_prn_admin

app_name = "meta_prn"

urlpatterns = [
    path("admin/", meta_prn_admin.urls),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
