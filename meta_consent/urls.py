from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import meta_consent_admin

app_name = "meta_consent"

urlpatterns = [
    path("admin/", meta_consent_admin.urls),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]
