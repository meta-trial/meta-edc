from edc_auth import (
    AUDITOR,
    CLINIC,
    SCREENING,
    UNBLINDING_REQUESTORS,
    UNBLINDING_REVIEWERS,
    get_default_codenames_by_group,
)
from sarscov2.auth import SARSCOV2, sarscov2_codenames

from meta_edc.meta_version import get_meta_version

from .codenames import (
    auditor,
    clinic,
    screening,
    unblinding_requestors,
    unblinding_reviewers,
)


def get_codenames_by_group():
    codenames_by_group = {k: v for k, v in get_default_codenames_by_group().items()}
    codenames_by_group[AUDITOR] = auditor
    codenames_by_group[CLINIC] = clinic
    codenames_by_group[SCREENING] = screening
    codenames_by_group[UNBLINDING_REQUESTORS] = unblinding_requestors
    codenames_by_group[UNBLINDING_REVIEWERS] = unblinding_reviewers
    if get_meta_version() == 2:
        codenames_by_group[SARSCOV2] = sarscov2_codenames
    return codenames_by_group
