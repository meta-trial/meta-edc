from copy import deepcopy

from django.db.utils import IntegrityError
from django.test import TestCase, tag
from edc_constants.constants import BLACK, FEMALE, NO, NOT_APPLICABLE, TBD, YES
from edc_utils.date import get_utcnow

from meta_edc.meta_version import PHASE_THREE, get_meta_version
from meta_screening.models import ScreeningPartOne

from ..options import get_part_one_eligible_options


@tag("el")
class TestSubjectScreeningPartOneModel(TestCase):
    def test_defaults(self):
        obj = ScreeningPartOne(
            hospital_identifier="111",
            initials="ZZ",
            gender=FEMALE,
            age_in_years=25,
            ethnicity=BLACK,
        )
        obj.save()
        self.assertEqual(obj.eligible_part_one, TBD)
        self.assertTrue(obj.reasons_ineligible_part_one is None)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)
        self.assertIsNotNone(obj.screening_identifier)

    def test_hospital_id_integrity(self):

        hospital_identifier = "111"
        obj = ScreeningPartOne(age_in_years=25, hospital_identifier=hospital_identifier)
        obj.save()

        obj = ScreeningPartOne(age_in_years=25, hospital_identifier=hospital_identifier)
        try:
            obj.save()
        except IntegrityError:
            pass
        else:
            self.fail("IntegrityError unexpectedly not raised.")

    def test_eligible(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        obj = ScreeningPartOne(**part_one_eligible_options)
        obj.save()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertTrue(obj.reasons_ineligible_part_one == "")

    def test_ineligible(self):
        if get_meta_version() == PHASE_THREE:
            staying_nearby = "staying_nearby_12"
        else:
            staying_nearby = "staying_nearby_6"
        opts = dict(
            report_datetime=get_utcnow(),
            hospital_identifier="111",
            initials="ZZ",
            gender=FEMALE,
            age_in_years=25,
            ethnicity=BLACK,
            hiv_pos=YES,
            art_six_months=YES,
            on_rx_stable=YES,
            lives_nearby=YES,
            pregnant=NOT_APPLICABLE,
        )
        opts.update({staying_nearby: NO})
        obj = ScreeningPartOne(**opts)
        obj.save()
        self.assertEqual(obj.eligible_part_one, NO)
        self.assertIn(
            "Unable/Unwilling to stay nearby", obj.reasons_ineligible_part_one
        )
        setattr(obj, staying_nearby, YES)
        obj.save()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertTrue(obj.reasons_ineligible_part_one == "")
