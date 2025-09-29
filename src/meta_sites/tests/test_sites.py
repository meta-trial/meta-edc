from django.test import TestCase
from edc_sites.exceptions import InvalidSiteError
from edc_sites.site import sites


class SiteTests(TestCase):
    def test_all(self):
        self.assertEqual(sites.get_by_attr("name", "hindu_mandal").site_id, 10)
        self.assertEqual(sites.get_by_attr("name", "amana").site_id, 20)

    def test_bad(self):
        self.assertRaises(InvalidSiteError, sites.get_by_attr, "name", "erik")
