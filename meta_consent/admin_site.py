from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

meta_consent_admin = EdcAdminSite(name="meta_consent_admin", app_label=AppConfig.name)
