from tempfile import mkdtemp

from django.test import TestCase, tag
from edc_reportable import ParserError, site_reportables


class TestReportables(TestCase):
    def test(self):
        try:
            from meta_labs import reportables
        except ParserError:
            self.fail("ParserError unexpectedly raised.")
        self.assertIsNotNone(site_reportables.get("meta"))
        filename1, filename2 = site_reportables.to_csv("meta", path=mkdtemp())
        print(filename1)
        print(filename2)
