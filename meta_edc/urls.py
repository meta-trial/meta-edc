from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls.conf import include, path, re_path
from django.views.defaults import page_not_found, server_error  # noqa
from django.views.generic import RedirectView
from edc_dashboard.views import AdministrationView
from edc_utils.paths_for_urlpatterns import paths_for_urlpatterns

from .views import HomeView


def trigger_error(request):
    division_by_zero = 1 / 0  # noqa


handler403 = "edc_dashboard.views.edc_handler403"
handler404 = "edc_dashboard.views.edc_handler404"

if settings.SENTRY_ENABLED:
    handler500 = "edc_dashboard.views.error_handlers.sentry.handler500"
else:
    handler500 = "edc_dashboard.views.edc_handler500"

# admin.site.final_catch_all_view = False

urlpatterns = [
    path("sentry-debug/", trigger_error),
    path("accounts/", include("edc_auth.urls")),
    path("administration/", AdministrationView.as_view(), name="administration_url"),
    path("subject/", include("meta_dashboard.urls")),
    *paths_for_urlpatterns("edc_action_item"),
    *paths_for_urlpatterns("edc_adverse_event"),
    *paths_for_urlpatterns("edc_appointment"),
    *paths_for_urlpatterns("edc_consent"),
    *paths_for_urlpatterns("edc_crf"),
    *paths_for_urlpatterns("edc_dashboard"),
    *paths_for_urlpatterns("edc_data_manager"),
    *paths_for_urlpatterns("edc_device"),
    *paths_for_urlpatterns("edc_export"),
    *paths_for_urlpatterns("edc_facility"),
    *paths_for_urlpatterns("edc_identifier"),
    *paths_for_urlpatterns("edc_lab"),
    *paths_for_urlpatterns("edc_lab_dashboard"),
    *paths_for_urlpatterns("edc_label"),
    *paths_for_urlpatterns("edc_locator"),
    *paths_for_urlpatterns("edc_metadata"),
    *paths_for_urlpatterns("edc_notification"),
    *paths_for_urlpatterns("edc_offstudy"),
    *paths_for_urlpatterns("edc_pdutils"),
    *paths_for_urlpatterns("edc_pharmacy"),
    *paths_for_urlpatterns("edc_protocol"),
    *paths_for_urlpatterns("edc_randomization"),
    *paths_for_urlpatterns("edc_reference"),
    *paths_for_urlpatterns("edc_refusal"),
    *paths_for_urlpatterns("edc_registration"),
    *paths_for_urlpatterns("edc_subject_dashboard"),
    *paths_for_urlpatterns("edc_visit_schedule"),
    *paths_for_urlpatterns("meta_ae"),
    *paths_for_urlpatterns("meta_consent"),
    *paths_for_urlpatterns("meta_export"),
    *paths_for_urlpatterns("meta_lists"),
    *paths_for_urlpatterns("meta_prn"),
    *paths_for_urlpatterns("meta_screening"),
    *paths_for_urlpatterns("meta_subject"),
    *paths_for_urlpatterns("sarscov2"),
]

if settings.DEFENDER_ENABLED:
    urlpatterns.append(
        path("defender/", include("defender.urls")),  # defender admin
    )

urlpatterns += [
    path("admin/", admin.site.urls),
    path(
        "switch_sites/",
        LogoutView.as_view(next_page=settings.INDEX_PAGE),
        name="switch_sites_url",
    ),
    path("home/", HomeView.as_view(), name="home_url"),
    re_path(".", RedirectView.as_view(url="/"), name="home_url"),
    re_path("", HomeView.as_view(), name="home_url"),
]
