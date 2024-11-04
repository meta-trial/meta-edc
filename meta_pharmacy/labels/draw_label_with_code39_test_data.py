from django.apps import apps as django_apps
from edc_constants.constants import FEMALE


def draw_label_with_code39_test_data() -> dict:
    container_type_model_cls = django_apps.get_model("edc_pharmacy.containertype")
    container_model_cls = django_apps.get_model("edc_pharmacy.container")
    request_model_cls = django_apps.get_model("edc_pharmacy.request")
    site_model_cls = django_apps.get_model("sites.site")
    container_type = container_type_model_cls(name="bottle")
    container = container_model_cls(
        name="bottle of 128", container_type=container_type, qty=128
    )
    return dict(
        request=request_model_cls(container=container),
        subject_identifier="999-99999-9",
        gender=FEMALE,
        sid=9999,
        code="A9B8C7",
        site=site_model_cls.objects.all()[0],
    )
