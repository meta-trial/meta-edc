from django.apps import apps as django_apps

META_AUDITOR = "META_AUDITOR"
META_CLINIC = "META_CLINIC"
META_CLINIC_SUPER = "META_CLINIC_SUPER"
META_EXPORT = "META_EXPORT"

clinic_codenames = []
autocomplete_models = []
clinic_auditor_codenames = []


for app_config in django_apps.get_app_configs():
    if app_config.name in [
        "meta_lists",
    ]:
        for model_cls in app_config.get_models():
            for prefix in ["view"]:
                clinic_codenames.append(
                    f"{app_config.name}.{prefix}_{model_cls._meta.model_name}"
                )
                clinic_auditor_codenames.append(
                    f"{app_config.name}.{prefix}_{model_cls._meta.model_name}"
                )

for app_config in django_apps.get_app_configs():
    if app_config.name in [
        "meta_prn",
        "meta_subject",
        "meta_consent",
    ]:
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower:
                clinic_codenames.append(f"{app_config.name}.view_{model_cls._meta.model_name}")
                clinic_auditor_codenames.append(
                    f"{app_config.name}.view_{model_cls._meta.model_name}"
                )
            elif model_cls._meta.label_lower in autocomplete_models:
                clinic_codenames.append(f"{app_config.name}.view_{model_cls._meta.model_name}")
            else:
                for prefix in ["add_", "change_", "view_", "delete_"]:
                    clinic_codenames.append(
                        f"{app_config.name}.{prefix}{model_cls._meta.model_name}"
                    )
clinic_codenames.sort()

ae_local_reviewer = [
    "meta_subject.add_aelocalreview",
    "meta_subject.change_aelocalreview",
    "meta_subject.delete_aelocalreview",
    "meta_subject.view_aelocalreview",
    "meta_subject.view_historicalaelocalreview",
]
ae_sponsor_reviewer = [
    "meta_subject.add_aesponsorreview",
    "meta_subject.change_aesponsorreview",
    "meta_subject.delete_aesponsorreview",
    "meta_subject.view_aesponsorreview",
    "meta_subject.view_historicalaesponsorreview",
]
