from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_constants.constants import YES

from meta_edc.meta_version import PHASE_TWO, get_meta_version

from .icp_referral import IcpReferral
from .proxy_models import ScreeningPartThree


class IcpReferralError(Exception):
    pass


def refer_to_icp(obj):
    """
    1.    FBG ≥ 126mg/dl (7.0 mmol/l) OR,
    2.    OGTT 2-h PG ≥ 200mg/dl (11.1 mmol/l) during OGTT OR,
    3.    HbA1c ≥ 6.5% (48 mmol/mol).13

    """
    if get_meta_version() != PHASE_TWO:
        raise IcpReferralError("ICP referral for META2 only. Got 3")
    fbg_value = False
    ogtt_value = False
    hba1c_value = False
    if obj.converted_fbg_value and obj.converted_fbg_value >= 7.0:
        fbg_value = True
    if obj.converted_ogtt_value and obj.converted_ogtt_value >= 11.1:
        ogtt_value = True
    if obj.hba1c_value and obj.hba1c_value >= 6.5:
        hba1c_value = True
    meets_lab_criteria = fbg_value or ogtt_value or hba1c_value
    meets_hiv_criteria = obj.hiv_pos == YES and obj.art_six_months == YES
    if obj.age_in_years >= 18 and meets_lab_criteria and meets_hiv_criteria:
        return True
    return False


def update_or_create_icp_referral(obj):
    if get_meta_version() != PHASE_TWO:
        raise IcpReferralError("ICP referral for META2 only. Got 3")
    referral_reasons = []
    if obj.converted_fbg_value and obj.converted_fbg_value >= 7.0:
        referral_reasons.append("FBG >= 7.0")
    if obj.converted_ogtt_value and obj.converted_ogtt_value >= 11.1:
        referral_reasons.append("OGTT >= 11.1")
    if obj.hba1c_value and obj.hba1c_value >= 6.5:
        referral_reasons.append("HbA1c >= 6.5")

    opts = dict(
        subject_screening=obj,
        age_in_years=obj.age_in_years,
        art_six_months=obj.art_six_months,
        ethnicity=obj.ethnicity,
        fbg_value=obj.converted_fbg_value,
        gender=obj.gender,
        hba1c_value=obj.hba1c_value,
        hiv_pos=obj.hiv_pos,
        hospital_identifier=obj.hospital_identifier,
        initials=obj.initials,
        meta_eligible=obj.eligible,
        meta_eligibility_datetime=obj.eligibility_datetime,
        ogtt_value=obj.converted_ogtt_value,
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

    PHASE_TWO only.
    """
    if not raw:
        if not instance.eligible:
            if get_meta_version() == PHASE_TWO:
                if refer_to_icp(instance):
                    update_or_create_icp_referral(instance)
                else:
                    IcpReferral.objects.filter(subject_screening=instance).delete()
