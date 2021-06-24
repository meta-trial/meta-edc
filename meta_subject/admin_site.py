from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

meta_subject_admin = EdcAdminSite(name="meta_subject_admin", app_label=AppConfig.name)
