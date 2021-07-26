"""Michigan Neuropathy Screening Instrument (MNSI) calculators."""
from edc_constants.constants import ABSENT, NO, PRESENT, YES

from meta_subject.constants import DECREASED, PRESENT_REINFORCEMENT, REDUCED


def patient_history_score(obj: object) -> int:
    """Returns MSNI score based on patient history questionnaire.

    Scoring based on:
        https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3641573/#S6title
    """
    # 1 point added for each 'YES' response for following Qs
    score = [
        obj.xnumb_legs_feet,  # Q1
        obj.burning_pain_legs_feet,  # Q2
        obj.feet_sensitive_touch,  # Q3
        obj.prickling_feelings_legs_feet,  # Q5
        obj.covers_touch_skin_painful,  # Q6
        obj.open_sore_foot_history,  # Q8
        obj.diabetic_neuropathy,  # Q9
        obj.symptoms_worse_night,  # Q11
        obj.legs_hurt_when_walk,  # Q12
        obj.skin_cracks_open_feet,  # Q14
        obj.amputation,  # Q15
    ].count(YES)

    # 1 point added for each 'NO' response for following Qs
    score += [
        obj.differentiate_hot_cold_water,  # Q7
        obj.sense_feet_when_walk,  # Q13
    ].count(NO)

    # Note: Questions 4 (muscle_cramps_legs_feet) and 10 (feel_weak)
    # not included in scoring algorithm
    return score


def physical_assessment_score(obj: object) -> float:
    """Returns score based on lower extremity examination.

    Scoring based on:
        https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3641573/#S6title
        (plus up to 2 extra points for monofilament assessments)
    """
    score = [
        obj.normal_appearance_right_foot,
        obj.normal_appearance_left_foot,
    ].count(NO)

    score += [obj.ulceration_right_foot, obj.ulceration_left_foot].count(PRESENT)

    for assessment in [
        obj.ankle_reflexes_right_foot,
        obj.ankle_reflexes_left_foot,
    ]:
        if assessment == PRESENT_REINFORCEMENT:
            score += 0.5
        elif assessment == ABSENT:
            score += 1

    for assessment in [
        obj.vibration_perception_right_toe,
        obj.vibration_perception_left_toe,
    ]:
        if assessment == DECREASED:
            score += 0.5
        elif assessment == ABSENT:
            score += 1

    for assessment in [obj.monofilament_right_foot, obj.monofilament_left_foot]:
        if assessment == REDUCED:
            score += 0.5
        elif assessment == ABSENT:
            score += 1

    return float(score)
