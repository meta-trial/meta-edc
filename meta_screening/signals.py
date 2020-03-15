from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_constants.constants import YES

from .models import IcpReferral, ScreeningPartThree


def refer_to_icp(obj):
    """
    1.    Fasting plasma glucose ≥ 126mg/dl (7.0 mmol/l) OR,
    2.    2-h PG ≥ 200mg/dl (11.1 mmol/l) during OGTT OR,
    3.    HbA1c ≥ 6.5% (48 mmol/mol).13

    """
    fasting_glucose = False
    ogtt_two_hr = False
    hba1c = False
    if obj.converted_fasting_glucose and obj.converted_fasting_glucose >= 7.0:
        fasting_glucose = True
    if obj.converted_ogtt_two_hr and obj.converted_ogtt_two_hr >= 11.1:
        ogtt_two_hr = True
    if obj.hba1c and obj.hba1c >= 6.5:
        hba1c = True
    meets_lab_criteria = fasting_glucose or ogtt_two_hr or hba1c
    meets_hiv_criteria = obj.hiv_pos == YES and obj.art_six_months == YES
    if obj.age_in_years >= 18 and meets_lab_criteria and meets_hiv_criteria:
        return True
    return False


def update_or_create_icp_referral(obj):
    referral_reasons = []
    if obj.converted_fasting_glucose and obj.converted_fasting_glucose >= 7.0:
        referral_reasons.append("fasting glucose >= 7.0")
    if obj.converted_ogtt_two_hr and obj.converted_ogtt_two_hr >= 11.1:
        referral_reasons.append("ogtt 2hr >= 11.1")
    if obj.hba1c and obj.hba1c >= 6.5:
        referral_reasons.append("HbA1c >= 6.5")

    opts = dict(
        subject_screening=obj,
        age_in_years=obj.age_in_years,
        art_six_months=obj.art_six_months,
        ethnicity=obj.ethnicity,
        fasting_glucose=obj.converted_fasting_glucose,
        gender=obj.gender,
        hba1c=obj.hba1c,
        hiv_pos=obj.hiv_pos,
        hospital_identifier=obj.hospital_identifier,
        initials=obj.initials,
        meta_eligible=obj.eligible,
        meta_eligibility_datetime=obj.eligibility_datetime,
        ogtt_two_hr=obj.converted_ogtt_two_hr,
        screening_identifier=obj.screening_identifier,
        referral_reasons="|".join(referral_reasons),
    )
    try:
        icp_referral = IcpReferral.objects.get(subject_screening=obj)
    except ObjectDoesNotExist:
        icp_referral = IcpReferral.objects.create(**opts)
    else:
        for k, v in opts.items():
            setattr(icp_referral, k, v)
        icp_referral.save()
    return icp_referral


@receiver(
    post_save,
    weak=False,
    sender=ScreeningPartThree,
    dispatch_uid="refer_to_icp_on_post_save",
)
def refer_to_icp_on_post_save(sender, instance, raw, created, **kwargs):
    """Refer to ICP if subject meets criteria.
    """
    if not raw:
        if not instance.eligible and instance.eligibility_datetime:
            if refer_to_icp(instance):
                update_or_create_icp_referral(instance)
            else:
                IcpReferral.objects.filter(subject_screening=instance).delete()
