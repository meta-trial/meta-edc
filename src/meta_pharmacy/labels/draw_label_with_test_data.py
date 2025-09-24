from django.apps import apps as django_apps
from django.utils import timezone


def draw_label_with_test_data() -> dict:
    receive_model_cls = django_apps.get_model("edc_pharmacy.receive")
    receive_item_model_cls = django_apps.get_model("edc_pharmacy.receiveitem")
    location_model_cls = django_apps.get_model("edc_pharmacy.location")
    lot_model_cls = django_apps.get_model("edc_pharmacy.lot")
    container_type_model_cls = django_apps.get_model("edc_pharmacy.containertype")
    container_model_cls = django_apps.get_model("edc_pharmacy.container")
    container_type = container_type_model_cls(name="bottle")
    container = container_model_cls(
        name="bottle of 128", container_type=container_type, qty=128
    )
    return dict(
        subject_identifier="999-99999-9",
        code="A9B8C7",
        location=location_model_cls.objects.filter(site__isnull=False).first(),
        container=container,
        lot=lot_model_cls(lot_no="999999999", expiration_date=timezone.now().date()),
        receive_item=receive_item_model_cls(
            receive=receive_model_cls(receive_identifier="99999999"),
            receive_item_identifier="99999999",
        ),
    )
