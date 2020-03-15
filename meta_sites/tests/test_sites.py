from django.test import TestCase
from edc_sites import get_site_id, InvalidSiteError

from ..sites import meta_sites


class SiteTests(TestCase):
    def test_all(self):
        self.assertEqual(get_site_id("reviewer", sites=meta_sites), 1)
        self.assertEqual(get_site_id("hindu_mandal", sites=meta_sites), 10)
        self.assertEqual(get_site_id("amana", sites=meta_sites), 20)

    def test_bad(self):
        self.assertRaises(InvalidSiteError, get_site_id, "erik", sites=meta_sites)
