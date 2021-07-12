PHASE_TWO = 2
PHASE_THREE = 3


def get_meta_version():
    from django.conf import settings

    return settings.META_PHASE
