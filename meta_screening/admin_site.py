from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

meta_screening_admin = EdcAdminSite(name="meta_screening_admin", app_label=AppConfig.name)
