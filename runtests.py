#!/usr/bin/env python
from datetime import datetime

import django
import logging
import os
import sys

from dateutil.tz import gettz
from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings
from os.path import abspath, dirname, join

from multisite import SiteID

app_name = "meta_edc"
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    EDC_AUTH_CODENAMES_WARN_ONLY=True,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    SITE_ID=SiteID(default=10),
    SENTRY_ENABLED=False,
    INDEX_PAGE="localhost:8000",
    EXPORT_FOLDER=join(base_dir, "tests", "export"),
    SUBJECT_SCREENING_MODEL="meta_screening.subjectscreening",
    SUBJECT_VISIT_MODEL="meta_subject.subjectvisit",
    SUBJECT_CONSENT_MODEL="meta_consent.subjectconsent",
    SUBJECT_REQUISITION_MODEL=f"meta_subject.subjectrequisition",
    DJANGO_LAB_DASHBOARD_REQUISITION_MODEL="meta_subject.subjectrequisition",
    ADVERSE_EVENT_ADMIN_SITE="meta_ae_admin",
    ADVERSE_EVENT_APP_LABEL="meta_ae",
    EDC_NAVBAR_DEFAULT="meta_dashboard",
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=datetime(
        2019, 6, 30, 0, 0, 0, tzinfo=gettz("UTC")
    ),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=datetime(
        2023, 12, 31, 23, 59, 59, tzinfo=gettz("UTC")
    ),
    DJANGO_LANGUAGES=dict(en="English", lg="Luganda", rny="Runyankore",),
    DASHBOARD_BASE_TEMPLATES=dict(
        edc_base_template="edc_dashboard/base.html",
        listboard_base_template="meta_edc/base.html",
        dashboard_base_template="meta_edc/base.html",
        screening_listboard_template="meta_dashboard/screening/listboard.html",
        subject_listboard_template="meta_dashboard/subject/listboard.html",
        subject_dashboard_template="meta_dashboard/subject/dashboard.html",
        subject_review_listboard_template="edc_review_dashboard/subject_review_listboard.html",
    ),
    ETC_DIR=os.path.join(base_dir, "tests", "etc"),
    EDC_BOOTSTRAP=3,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_CONTACTS={
        "data_request": "someone@example.com",
        "data_manager": "someone@example.com",
        "tmg": "someone@example.com",
    },
    EMAIL_ENABLED=True,
    HOLIDAY_FILE=join(base_dir, "tests", "holidays.csv"),
    LIVE_SYSTEM=False,
    EDC_RANDOMIZATION_LIST_PATH=join(base_dir, "tests", "etc"),
    EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=True,
    EDC_SITES_MODULE_NAME="meta_sites",
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django_crypto_fields.apps.AppConfig",
        "django_revision.apps.AppConfig",
        # "debug_toolbar",
        "django_extensions",
        "django_celery_results",
        "django_celery_beat",
        "logentry_admin",
        "simple_history",
        "storages",
        "corsheaders",
        "rest_framework",
        "rest_framework.authtoken",
        # "django_collect_offline.apps.AppConfig",
        # "django_collect_offline_files.apps.AppConfig",
        "edc_action_item.apps.AppConfig",
        "edc_adverse_event.apps.AppConfig",
        "edc_appointment.apps.AppConfig",
        "edc_auth.apps.AppConfig",
        "edc_model_wrapper.apps.AppConfig",
        "edc_crf.apps.AppConfig",
        "edc_data_manager.apps.AppConfig",
        "edc_consent.apps.AppConfig",
        "edc_device.apps.AppConfig",
        "edc_dashboard.apps.AppConfig",
        "edc_export.apps.AppConfig",
        "edc_facility.apps.AppConfig",
        "edc_fieldsets.apps.AppConfig",
        "edc_form_validators.apps.AppConfig",
        "edc_lab.apps.AppConfig",
        "edc_lab_dashboard.apps.AppConfig",
        "edc_label.apps.AppConfig",
        "edc_locator.apps.AppConfig",
        "edc_reference.apps.AppConfig",
        "edc_reports.apps.AppConfig",
        "edc_identifier.apps.AppConfig",
        "edc_metadata.apps.AppConfig",
        "edc_metadata_rules.apps.AppConfig",
        "edc_model_admin.apps.AppConfig",
        "edc_navbar.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_offstudy.apps.AppConfig",
        "edc_visit_tracking.apps.AppConfig",
        "edc_visit_schedule.apps.AppConfig",
        "edc_pdutils.apps.AppConfig",
        "edc_pharmacy.apps.AppConfig",
        # "edc_pharmacy_dashboard.apps.AppConfig",
        "edc_prn.apps.AppConfig",
        "edc_randomization.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_subject_dashboard.apps.AppConfig",
        "edc_timepoint.apps.AppConfig",
        "edc_list_data.apps.AppConfig",
        "edc_review_dashboard.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "sarscov2.apps.AppConfig",
        "meta_auth.apps.AppConfig",
        "meta_consent.apps.AppConfig",
        "meta_lists.apps.AppConfig",
        "meta_dashboard.apps.AppConfig",
        "meta_labs.apps.AppConfig",
        "meta_metadata_rules.apps.AppConfig",
        "meta_reference.apps.AppConfig",
        "meta_subject.apps.AppConfig",
        "meta_form_validators.apps.AppConfig",
        "meta_visit_schedule.apps.AppConfig",
        "meta_ae.apps.AppConfig",
        "meta_prn.apps.AppConfig",
        "meta_export.apps.AppConfig",
        "meta_screening.apps.AppConfig",
        "meta_edc.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    add_adverse_event_dashboard_middleware=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failfast = True if [t for t in sys.argv if t == "--failfast"] else False
    failures = DiscoverRunner(failfast=failfast, tags=tags).run_tests(
        [
            "tests",
            "meta_ae.tests",
            "meta_auth.tests",
            "meta_lists.tests",
            "meta_dashboard.tests",
            "meta_labs.tests",
            "meta_metadata_rules.tests",
            "meta_reference.tests",
            "meta_subject.tests",
            "meta_form_validators.tests",
            "meta_visit_schedule.tests",
            "meta_ae.tests",
            "meta_prn.tests",
            "meta_export.tests",
            "meta_screening.tests",
        ]
    )
    sys.exit(bool(failures))


if __name__ == "__main__":
    logging.basicConfig()
    main()
