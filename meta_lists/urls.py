from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "meta_lists"

urlpatterns = [
    path("", RedirectView.as_view(url="/meta_lists_admin/"), name="home_url"),
]
