from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

meta_lists_admin = EdcAdminSite(name="meta_lists_admin", app_label=AppConfig.name)
