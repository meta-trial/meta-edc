from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.core.management import BaseCommand
from edc_egfr.egfr import Egfr
from edc_utils import convert_php_dateformat, get_utcnow
from edc_utils.round_up import round_half_away_from_zero
from edc_visit_schedule.constants import DAY1
from edc_visit_schedule.utils import is_baseline
from tqdm import tqdm


def update_egfr():
    rft_model_cls = django_apps.get_model("meta_subject.bloodresultsrft")
    registered_subject_model_cls = django_apps.get_model("edc_registration.RegisteredSubject")
    subject_visit_model_cls = django_apps.get_model("meta_subject.subjectvisit")
    total = rft_model_cls.objects.all().count()
    updated = 0
    modified = get_utcnow()
    for obj in tqdm(rft_model_cls.objects.all(), total=total):
        if is_baseline(obj.related_visit):
            baseline_egfr_value = None
        else:
            baseline_visit = subject_visit_model_cls.objects.get(
                subject_identifier=obj.related_visit.subject_identifier,
                visit_code=DAY1,
                visit_code_sequence=0,
            )
            baseline_egfr_value = rft_model_cls.objects.get(
                subject_visit_id=baseline_visit.id
            ).egfr_value
        rs = registered_subject_model_cls.objects.get(
            subject_identifier=obj.related_visit.subject_identifier
        )
        egfr_options = dict(
            dob=rs.dob,
            gender=rs.gender,
            ethnicity=rs.ethnicity,
            value_threshold=45.0000,
            report_datetime=obj.report_datetime,
            baseline_egfr_value=baseline_egfr_value,
            formula_name="ckd-epi",
            reference_range_collection_name="meta",
            subject_visit=obj.related_visit,
            creatinine_units=obj.creatinine_units,
            creatinine_value=obj.creatinine_value,
            assay_datetime=obj.assay_datetime,
        )
        egfr = Egfr(percent_drop_threshold=20.0000, **egfr_options)
        if round_half_away_from_zero(obj.egfr_value, 4) != round_half_away_from_zero(
            egfr.egfr_value, 4
        ):
            obj.egfr_value = egfr.egfr_value
            obj.egfr_units = egfr.egfr_units
            obj.egfr_grade = egfr.egfr_grade
            obj.egfr_drop_value = egfr.egfr_drop_value
            obj.egfr_drop_units = egfr.egfr_drop_units
            obj.egfr_drop_grade = egfr.egfr_drop_grade
            obj.modified = modified
            try:
                obj.save_base()
            except MultipleObjectsReturned:
                print(
                    obj.subject_visit.subject_identifier,
                    obj.subject_visit.visit_code,
                    obj.subject_visit.visit_code_sequence,
                )
            else:
                updated += 1

    print(
        f"Done. Updated `{updated}` blood results RFT CRFs. TIMESTAMP is "
        f"`{modified.strftime(convert_php_dateformat(settings.DATETIME_FORMAT))}`"
    )


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_egfr()
