from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

meta_ae_admin = EdcAdminSite(name="meta_ae_admin", app_label=AppConfig.name)
