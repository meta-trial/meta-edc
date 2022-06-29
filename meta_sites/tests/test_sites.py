from django.test import TestCase
from edc_sites import InvalidSiteError, get_site_id

from ..sites import all_sites


class SiteTests(TestCase):
    def test_all(self):

        self.assertEqual(get_site_id("hindu_mandal", sites=all_sites.get("tanzania")), 10)
        self.assertEqual(get_site_id("amana", sites=all_sites.get("tanzania")), 20)

    def test_bad(self):
        self.assertRaises(
            InvalidSiteError, get_site_id, "erik", sites=all_sites.get("tanzania")
        )
