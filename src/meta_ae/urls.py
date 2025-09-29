from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "meta_ae"

urlpatterns = [
    path("", RedirectView.as_view(url="/meta_ae/admin/"), name="home_url"),
]
