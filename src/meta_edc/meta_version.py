PHASE_TWO = 2
PHASE_THREE = 3
PHASE_THREE_ONLY = "PHASE_THREE_ONLY"


class InvalidMetaVersion(Exception):
    pass


def get_meta_version():
    from django.conf import settings

    return settings.META_PHASE
