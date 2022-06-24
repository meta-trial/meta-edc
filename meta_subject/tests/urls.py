from django.contrib.auth import admin
from django.urls.conf import include, path
from django.views.generic.base import RedirectView

from meta_ae.admin_site import meta_ae_admin

urlpatterns = [
    path("admin/", meta_ae_admin.urls),
    path("admin/", admin.site.urls),
    path("accounts/", include("edc_auth.urls")),
    path("edc_adverse_event/", include("edc_adverse_event.urls")),
    path("edc_auth/", include("edc_auth.urls")),
    path("edc_consent/", include("edc_consent.urls")),
    path("edc_dashboard/", include("edc_dashboard.urls")),
    path("edc_device/", include("edc_device.urls")),
    path("edc_export/", include("edc_export.urls")),
    path("edc_protocol/", include("edc_protocol.urls")),
    path("edc_randomization/", include("edc_randomization.urls")),
    path("edc_reference/", include("edc_reference.urls")),
    path("edc_visit_schedule/", include("edc_visit_schedule.urls")),
    path("ae/", include("meta_ae.urls")),
    path("meta_consent/", include("meta_consent.urls")),
    path("administration", RedirectView.as_view(url="admin/"), name="administration_url"),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]
