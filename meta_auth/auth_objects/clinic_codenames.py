from django.apps import apps as django_apps

clinic_codenames = []
for app_config in django_apps.get_app_configs():
    if app_config.name in ["meta_lists", "meta_prn", "meta_subject"]:
        for model_cls in app_config.get_models():
            for prefix in ["add", "change", "delete", "view"]:
                clinic_codenames.append(
                    f"{app_config.name}.{prefix}_{model_cls._meta.model_name}"
                )
clinic_codenames.sort()
