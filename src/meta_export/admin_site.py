from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

meta_export_admin = EdcAdminSite(name="meta_export_admin", app_label=AppConfig.name)
