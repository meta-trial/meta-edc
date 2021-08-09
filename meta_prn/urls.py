from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "meta_prn"

urlpatterns = [
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
