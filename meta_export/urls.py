from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "meta_export"

urlpatterns = [
    path("", RedirectView.as_view(url="/meta_export/admin/"), name="home_url"),
]
