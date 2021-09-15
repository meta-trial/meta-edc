from edc_auth.site_auths import site_auths
from edc_screening.auth_objects import SCREENING, SCREENING_SUPER, SCREENING_VIEW

from .auth_objects import screening_codenames

site_auths.update_group(*screening_codenames, name=SCREENING, no_delete=True)
site_auths.update_group(*screening_codenames, name=SCREENING_SUPER)
site_auths.update_group(*screening_codenames, name=SCREENING_VIEW, view_only=True)
