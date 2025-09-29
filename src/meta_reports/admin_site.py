from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

meta_reports_admin = EdcAdminSite(name="meta_reports_admin", app_label=AppConfig.name)
