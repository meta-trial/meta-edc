from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

meta_spfq_admin = EdcAdminSite(name="meta_spfq_admin", app_label=AppConfig.name)
