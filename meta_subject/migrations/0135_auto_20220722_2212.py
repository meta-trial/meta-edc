# Generated by Django 3.2.11 on 2022-07-22 19:12
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from edc_egfr.calculators import EgfrCkdEpi, egfr_percent_change
from edc_visit_schedule.constants import DAY1
from tqdm import tqdm


def update_revised_egrf(apps, schema_editor):
    bloodresultrft_model_cls = apps.get_model("meta_subject.bloodresultsrft")
    subjectvisit_model_cls = apps.get_model("meta_subject.subjectvisit")
    try:
        subjectscreening_model_cls = apps.get_model("meta_screening.subjectscreening")
    except LookupError:
        pass
    else:
        total = bloodresultrft_model_cls.objects.all().count()
        for obj in tqdm(bloodresultrft_model_cls.objects.all(), total=total):
            subject_visit = subjectvisit_model_cls.objects.get(id=obj.subject_visit_id)
            subject_screening = subjectscreening_model_cls.objects.get(
                subject_identifier=subject_visit.subject_identifier
            )
            try:
                baseline_obj = bloodresultrft_model_cls.objects.get(
                    subject_visit__subject_identifier=subject_visit.subject_identifier,
                    subject_visit__visit_code=DAY1,
                    subject_visit__visit_code_sequence=0,
                )
            except ObjectDoesNotExist:
                pass
            else:
                obj.old_egfr_value = obj.egfr_value
                obj.old_egfr_drop_value = obj.egfr_drop_value
                obj.egfr_value = EgfrCkdEpi(
                    gender=subject_screening.gender,
                    ethnicity=subject_screening.ethnicity,
                    age_in_years=subject_screening.age_in_years,
                    creatinine_value=obj.creatinine_value,
                    creatinine_units=obj.creatinine_units,
                ).value
                obj.egfr_drop_value = egfr_percent_change(
                    float(obj.egfr_value), float(baseline_obj.egfr_value)
                )
                obj.save_base(
                    update_fields=[
                        "egfr_value",
                        "egfr_drop_value",
                        "old_egfr_value",
                        "old_egfr_drop_value",
                    ]
                )


class Migration(migrations.Migration):
    dependencies = [
        ("meta_subject", "0134_auto_20220722_2211"),
    ]

    operations = [migrations.RunPython(update_revised_egrf)]
