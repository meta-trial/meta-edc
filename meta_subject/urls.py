from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "meta_subject"

urlpatterns = [
    path("", RedirectView.as_view(url="/meta_subject/admin/"), name="home_url"),
]
