from edc_auth.site_auths import site_auths
from edc_screening.auth_objects import SCREENING

from .auth_objects import screening_codenames

site_auths.update_group(*screening_codenames, name=SCREENING)
