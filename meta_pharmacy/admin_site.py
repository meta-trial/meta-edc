from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

meta_pharmacy_admin = EdcAdminSite(
    name="meta_pharmacy_admin",
    app_label=AppConfig.name,
    keep_delete_action=True,
)
