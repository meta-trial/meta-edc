from django.core.exceptions import ImproperlyConfigured


def confirm_meta_version(phase):
    response = input(f"This is meta phase {phase}. Type 2 or 3 to continue: ")
    if response not in ["2", "3"]:
        print("settings load has been halted.")
        raise ImproperlyConfigured("Check settings.META_PHASE")
    return int(response)
