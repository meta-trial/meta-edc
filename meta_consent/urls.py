from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "meta_consent"

urlpatterns = [
    path("", RedirectView.as_view(url="/meta_consent_admin/"), name="home_url"),
]
