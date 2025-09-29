PHASE_TWO = 2
PHASE_THREE = 3
PHASE_THREE_ONLY = "PHASE_THREE_ONLY"


class InvalidMetaVersion(Exception):  # noqa: N818
    pass


def get_meta_version():
    from django.conf import settings  # noqa: PLC0415

    return settings.META_PHASE
