from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

meta_prn_admin = EdcAdminSite(name="meta_prn_admin", app_label=AppConfig.name)
