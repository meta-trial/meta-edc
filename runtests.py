import os
import sys

import django

app_name = "meta_edc"
tests = [
    "tests",
    "meta_ae.tests",
    "meta_consent.tests",
    "meta_dashboard.tests",
    "meta_edc.tests",
    "meta_labs.tests",
    "meta_lists.tests",
    "meta_prn.tests",
    "meta_rando.tests",
    "meta_screening.tests",
    "meta_subject.tests",
    "meta_visit_schedule.tests",
]
if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = f"{app_name}.tests.test_settings"
    django.setup()
    from django.test.runner import DiscoverRunner

    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failfast = any([True for t in sys.argv if t.startswith("--failfast")])
    keepdb = any([True for t in sys.argv if t.startswith("--keepdb")])
    skip_checks = any([True for t in sys.argv if t.startswith("--skip_checks")])
    opts = dict(failfast=failfast, tags=tags, keepdb=keepdb, skip_checks=skip_checks)
    failures = DiscoverRunner(**opts).run_tests(tests, **opts)
    sys.exit(failures)
