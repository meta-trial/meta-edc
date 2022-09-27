from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, override_settings
from edc_constants.constants import FEMALE, MALE
from edc_randomization.site_randomizers import site_randomizers
from edc_registration.models import RegisteredSubject

from meta_edc.meta_version import PHASE_THREE, get_meta_version
from meta_rando.randomizers import RandomizerPhaseThree
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin


class TestRandomizers(MetaTestCaseMixin, TestCase):

    import_randomization_list = False

    def test_import(self):
        RandomizerPhaseThree.import_list(sid_count_for_tests=10)
        obj = RandomizerPhaseThree.model_cls().objects.all().order_by("sid")[0]
        self.assertEqual(
            [1001, "active", "hindu_mandal", "F"],
            [obj.sid, obj.assignment, obj.site_name, obj.gender],
        )

    @override_settings(META_PHASE=PHASE_THREE)
    def test_randomize_phase_three(self):
        self.assertEqual(get_meta_version(), 3)
        site_randomizers._registry = {}
        site_randomizers.loaded = False
        site_randomizers.register(RandomizerPhaseThree)
        self.subject_visit = self.get_subject_visit(gender=FEMALE)
        try:
            RegisteredSubject.objects.get(
                sid=1001,
                subject_identifier=self.subject_visit.subject_identifier,
                gender=FEMALE,
            )
        except ObjectDoesNotExist:
            self.fail("RegisteredSubject unexpectedly does not exist")

        self.subject_visit = self.get_subject_visit(gender=MALE)
        try:
            RegisteredSubject.objects.get(
                sid=1003,
                subject_identifier=self.subject_visit.subject_identifier,
                gender=MALE,
            )
        except ObjectDoesNotExist:
            self.fail("RegisteredSubject unexpectedly does not exist")

        self.subject_visit = self.get_subject_visit(gender=FEMALE)
        try:
            RegisteredSubject.objects.get(
                sid=1002,
                subject_identifier=self.subject_visit.subject_identifier,
                gender=FEMALE,
            )
        except ObjectDoesNotExist:
            self.fail("RegisteredSubject unexpectedly does not exist")
