from django.db import models
from edc_constants.choices import DIFFICULT_TO_EASY_CHOICE, DISAGREE_TO_AGREE_CHOICE, YES_NO
from edc_model.models import BaseUuidModel

from ..choices import (
    LESS_EXPECTED_TO_MORE_EXPECTED_CHOICE,
    NOT_AT_ALL_TO_HIGHLY_CHOICE,
    NOT_AT_ALL_TO_SEVERE_CHOICE,
)
from ..model_mixins import CrfModelMixin


class Spfq(CrfModelMixin, BaseUuidModel):
    a01 = models.CharField(
        verbose_name="I understood the treatment process in this trial",
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
        help_text="for example: when and how to take or use a treatment",
    )
    a02 = models.CharField(
        verbose_name=(
            "The information given to me before "
            "I joined the trial was everything I wanted to know"
        ),
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
        help_text=(
            "for example: visits and procedures, "
            "time commitment, who to contact with questions"
        ),
    )
    a03 = models.CharField(
        verbose_name=(
            "The information given to me before I "
            "joined the trial was easy for me to understand"
        ),
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
        help_text=(
            "for example: visits and procedures, "
            "time commitment, who to contact with questions"
        ),
    )
    a04 = models.CharField(
        verbose_name=(
            "I felt comfortable that I could ask any questions before I joined the trial"
        ),
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
    )
    b01 = models.CharField(
        verbose_name="Overall I was satisfied with the trial site",
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
        help_text=(
            "for example: comfort and privacy of treatment area, "
            "waiting area, parking, ease of access to the site"
        ),
    )
    b02 = models.CharField(
        verbose_name="My trial visits were well organized",
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
    )
    b03 = models.CharField(
        verbose_name="My trial visits were scheduled at a convenient time for me",
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
    )
    b04 = models.CharField(
        verbose_name="The staff treated me with respect",
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
    )
    b05 = models.CharField(
        verbose_name="I felt comfortable that I could ask questions during the trial",
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
    )
    b06 = models.CharField(
        verbose_name=(
            "I was satisfied with the answers I have received to my questions during the trial"
        ),
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
    )
    b07 = models.CharField(
        verbose_name="The time taken to collect data was acceptable to me",
        max_length=25,
        choices=YES_NO,
        help_text="for example: in person visits, questionnaires, forms",
    )
    b08 = models.CharField(
        verbose_name="The impact the trial has had on my daily activities is acceptable",
        max_length=25,
        choices=YES_NO,
        help_text="for example: household chores, work commitments, eating",
    )
    b09 = models.CharField(
        verbose_name="The way in which trial data is being collected is acceptable to me",
        max_length=25,
        choices=YES_NO,
        help_text=(
            "for example: in person, online questionnaire, "
            "diary, wearable sensors, monitoring machines, technology"
        ),
    )
    b10 = models.CharField(
        verbose_name=(
            "Optional: I am being kept informed of the results of "
            "my medical tests done during the trial, including during screening"
        ),
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
        help_text="for example: blood tests, scans etc.",
    )

    c01 = models.CharField(
        verbose_name="I was informed when I had completed the trial",
        max_length=25,
        choices=YES_NO,
    )

    c02 = models.CharField(
        verbose_name=(
            "I was informed of any future opportunities to "
            "access the overall trial results if I wanted to"
        ),
        max_length=25,
        choices=YES_NO,
    )

    c03 = models.CharField(
        verbose_name="How easy was it to take the medication?",
        max_length=25,
        choices=DIFFICULT_TO_EASY_CHOICE,
    )

    c04 = models.CharField(
        verbose_name="Did you experience any burden or side effects?",
        max_length=25,
        choices=NOT_AT_ALL_TO_SEVERE_CHOICE,
    )

    c05 = models.CharField(
        verbose_name="How acceptable was it to take the drug?",
        max_length=25,
        choices=NOT_AT_ALL_TO_HIGHLY_CHOICE,
    )

    c06 = models.CharField(
        verbose_name="How easy was it to fit the medication into your routine?",
        max_length=25,
        choices=DIFFICULT_TO_EASY_CHOICE,
    )

    c07 = models.CharField(
        verbose_name="How burdensome was taking part in the trial?",
        max_length=25,
        choices=NOT_AT_ALL_TO_SEVERE_CHOICE,
    )

    c08 = models.CharField(
        verbose_name=(
            "Overall, I was satisfied with the information "
            "I received about future support after the trial"
        ),
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
        help_text="for example: future treatment, follow-up contact details",
    )

    c09 = models.CharField(
        verbose_name="Overall, I was satisfied with my trial experience",
        max_length=25,
        choices=DISAGREE_TO_AGREE_CHOICE,
    )

    c10 = models.CharField(
        verbose_name=(
            "Compared to when the trial started, the overall "
            "commitment required was similar to what I expected"
        ),
        max_length=25,
        choices=LESS_EXPECTED_TO_MORE_EXPECTED_CHOICE,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Feedback Questionnaire (SPFQ)"
        verbose_name_plural = "Feedback Questionnaires (SPFQ)"
