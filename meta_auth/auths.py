from edc_auth import AUDITOR, CLINIC, SCREENING
from edc_auth.site_auths import site_auths
from sarscov2.auth import SARSCOV2, sarscov2_codenames

from meta_edc.meta_version import get_meta_version

from .auth_objects import auditor, clinic, screening

site_auths.update_group(*auditor, name=AUDITOR)
site_auths.update_group(*clinic, name=CLINIC)
site_auths.add_group(*screening, name=SCREENING)
if get_meta_version() == 2:
    site_auths.add_group(*sarscov2_codenames, name=SARSCOV2)
