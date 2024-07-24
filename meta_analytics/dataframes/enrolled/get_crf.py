from __future__ import annotations

from typing import TYPE_CHECKING, Type

import pandas as pd
from django.apps import apps as django_apps
from django_pandas.io import read_frame

from ..utils import convert_dates_from_model, convert_numerics_from_model
from .get_subject_visit import get_subject_visit

if TYPE_CHECKING:
    from edc_crf.model_mixins import CrfModelMixin
    from edc_model.models import BaseUuidModel

    class MyModel(CrfModelMixin, BaseUuidModel):
        class Meta: ...  # noqa: E701


def get_crf(
    model: str | None = None,
    model_cls: Type[MyModel] | None = None,
    merge_visit: bool | None = None,
) -> pd.DataFrame:
    model_cls = model_cls or django_apps.get_model(model)
    qs = model_cls.objects.all()
    df = read_frame(qs)
    df.rename(columns={"subject_visit": "subject_visit_id"}, inplace=True)
    if merge_visit:
        df_subject_visit = get_subject_visit()
        df = pd.merge(
            df,
            df_subject_visit,
            on="subject_visit_id",
            how="left",
            suffixes=("", "_subject_visit"),
        )
        df.reset_index(drop=True, inplace=True)
    df = convert_numerics_from_model(df, model_cls)
    df = convert_dates_from_model(df, model_cls)
    return df
