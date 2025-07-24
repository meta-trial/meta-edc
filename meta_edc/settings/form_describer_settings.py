#!/usr/bin/env python
""" So `make_forms_reference` can be run in gh-actions without
an .env file.

    python manage.py make_forms_reference \
        --app-label meta_subject \
        --admin-site meta_subject_admin \
        --visit-schedule visit_schedule \
        --settings=tests.form_describer_settings
"""

import os
import sys
from importlib.metadata import version
from pathlib import Path

from edc_test_settings.default_test_settings import DefaultTestSettings

from .get_test_setting_opts import get_test_setting_opts

# from tests.test_setting_options import get_test_setting_opts

app_name = "meta_edc"
base_dir = Path(__file__).parent.parent.parent
opts = get_test_setting_opts(app_name, base_dir)
opts.update(
    # hack for forms-reference in gh-actions
    DJANGO_CRYPTO_FIELDS_KEY_PATH=base_dir / "tests" / "etc",
    DJANGO_CRYPTO_FIELDS_TEST_MODULE="--settings=meta_edc.settings.form_describer_settings",
    # hack for forms-reference in gh-actions
    SILENCED_SYSTEM_CHECKS=[
        "edc_sites.E001",
        "edc_sites.E002",
        "sites.E101",
        "edc_navbar.E002",
        "edc_navbar.E003",
    ],
    DJANGO_REVISION_IGNORE_WORKING_DIR=True,
    REVISION=version(app_name),
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", "mysql"),
            "USER": os.getenv("DB_USER", "root"),
            "PASSWORD": os.getenv("DB_PASSWORD", "mysql"),
            "HOST": os.getenv("DB_HOST", "mysql"),
            "PORT": os.getenv("DB_PORT", "3306"),
        }
    },
)
project_settings = DefaultTestSettings(**opts).settings

for k, v in project_settings.items():
    setattr(sys.modules[__name__], k, v)
