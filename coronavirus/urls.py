from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import coronavirus_admin

app_name = "coronavirus"

urlpatterns = [
    path("admin/", coronavirus_admin.urls),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
