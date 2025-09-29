import contextlib
import sys

from django.test import TestCase, tag
from edc_lab import site_labs
from edc_reportable.models import GradingData, NormalData, ReferenceRangeCollection
from edc_reportable.utils import load_reference_ranges

from meta_labs.reportables import (
    collection_name,
    grading_data,
    normal_data,
    reportable_grades,
    reportable_grades_exceptions,
)


class TestReportables(TestCase):
    @tag("37")
    def test_load_reference_ranges(self):
        load_reference_ranges(
            collection_name=collection_name,
            grading_data=grading_data,
            normal_data=normal_data,
            reportable_grades=reportable_grades,
            reportable_grades_exceptions=reportable_grades_exceptions,
        )
        self.assertTrue(ReferenceRangeCollection.objects.filter(name=collection_name).exists())
        reference_range_collection = ReferenceRangeCollection.objects.get(name=collection_name)

        for requisition_panel in site_labs.lab_profiles.get(
            "subject_lab_profile"
        ).panels.values():
            for utest_id in requisition_panel.utest_ids:
                with contextlib.suppress(ValueError):
                    utest_id, _ = utest_id  # noqa: PLW2901
                if not NormalData.objects.filter(label=utest_id).exists():
                    sys.stdout.write(f"{utest_id} does not exist in NormalData\n")
                if not GradingData.objects.filter(label=utest_id).exists():
                    sys.stdout.write(f"{utest_id} does not exist in GradingData\n")

        for requisition_panel in site_labs.lab_profiles.get(
            "subject_lab_profile"
        ).panels.values():
            for utest_id in requisition_panel.utest_ids:
                with contextlib.suppress(ValueError):
                    utest_id, _ = utest_id  # noqa: PLW2901
                self.assertTrue(
                    NormalData.objects.filter(label=utest_id).exists(),
                    msg=f"{utest_id} does not exist in NormalData",
                )
                self.assertTrue(
                    GradingData.objects.filter(label=utest_id).exists(),
                    msg=f"{utest_id} does not exist in GradingData",
                )

        self.assertEqual(
            NormalData.objects.filter(
                reference_range_collection=reference_range_collection
            ).count(),
            88,
        )
        self.assertEqual(
            GradingData.objects.filter(
                reference_range_collection=reference_range_collection
            ).count(),
            180,
        )
