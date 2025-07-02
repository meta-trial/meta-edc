from django.test import TestCase
from edc_reportable.models import GradingData, NormalData, ReferenceRangeCollection
from edc_reportable.utils import load_reference_ranges


class TestReportables(TestCase):
    def test_load_reference_ranges(self):

        from meta_labs.reportables import (
            collection_name,
            grading_data,
            normal_data,
            reportable_grades,
            reportable_grades_exceptions,
        )

        load_reference_ranges(
            collection_name=collection_name,
            grading_data=grading_data,
            normal_data=normal_data,
            reportable_grades=reportable_grades,
            reportable_grades_exceptions=reportable_grades_exceptions,
        )
        self.assertTrue(ReferenceRangeCollection.objects.filter(name=collection_name).exists())
        reference_range_collection = ReferenceRangeCollection.objects.get(name=collection_name)
        self.assertEqual(
            NormalData.objects.filter(
                reference_range_collection=reference_range_collection
            ).count(),
            82,
        )
        self.assertEqual(
            GradingData.objects.filter(
                reference_range_collection=reference_range_collection
            ).count(),
            174,
        )
