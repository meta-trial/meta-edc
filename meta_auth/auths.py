from edc_auth.auth_objects import AUDITOR, CLINIC, CLINIC_SUPER
from edc_auth.site_auths import site_auths
from sarscov2.auth import SARSCOV2, sarscov2_codenames

from meta_edc.meta_version import get_meta_version

from .auth_objects import auditor_codenames, clinic_codenames

site_auths.update_group(*auditor_codenames, name=AUDITOR)
site_auths.update_group(*clinic_codenames, name=CLINIC)
site_auths.update_group(*clinic_codenames, name=CLINIC_SUPER)

if get_meta_version() == 2:
    site_auths.add_group(*sarscov2_codenames, name=SARSCOV2)
