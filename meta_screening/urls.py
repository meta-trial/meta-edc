from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import meta_screening_admin

app_name = "meta_screening"

urlpatterns = [
    path("admin/", meta_screening_admin.urls),
    path("", RedirectView.as_view(url="/meta_screening/admin/"), name="home_url"),
]
