from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django_pylabels.models import LabelSpecification
from edc_pharmacy.models import (
    Assignment,
    Container,
    ContainerType,
    ContainerUnits,
    Formulation,
    Location,
    Product,
    Supplier,
)
from edc_pylabels.models import LabelConfiguration
from edc_pylabels.site_label_configs import site_label_configs


def update_initial_pharmacy_data():
    update_assignment()
    update_container()
    update_location()
    update_product()
    update_supplier()
    update_labels()


def update_assignment():
    for assignment in ["placebo", "active"]:
        try:
            Assignment.objects.get(name=assignment)
        except ObjectDoesNotExist:
            Assignment.objects.create(name=assignment, display_name=assignment.title())


def update_container():
    tablet_type = ContainerType.objects.get(name="tablet")
    bottle_type = ContainerType.objects.get(name="bottle")
    units = ContainerUnits.objects.get(name="tablet")
    opts = {
        "tablet": dict(
            name="tablet",
            display_name="Tablet",
            container_type=tablet_type,
            units=units,
            qty=1,
            may_order_as=True,
            max_per_subject=0,
        ),
        "bottle30k": dict(
            name="bottle30k",
            display_name="Bottle 30K",
            container_type=bottle_type,
            units=units,
            qty=30000,
            may_receive_as=True,
            max_per_subject=0,
        ),
        "bottle128": dict(
            name="bottle128",
            display_name="Bottle 128",
            container_type=bottle_type,
            units=units,
            qty=128,
            max_per_subject=3,
            may_repack_as=True,
            may_request_as=True,
            may_dispense_as=True,
        ),
    }
    for name, data in opts.items():
        try:
            Container.objects.get(name=name)
        except ObjectDoesNotExist:
            Container.objects.create(**data)


def update_location():
    for obj in Location.objects.exclude(name="central"):
        obj.site_id = Site.objects.get(name=obj.name).id
        obj.save(update_fields=["site_id"])


def update_product():
    formulation = Formulation.objects.get()
    active = Assignment.objects.get(name="active")
    placebo = Assignment.objects.get(name="placebo")
    try:
        Product.objects.get(formulation=formulation, assignment=active)
    except ObjectDoesNotExist:
        Product(assignment=active, formulation=formulation).save()
    try:
        Product.objects.get(formulation=formulation, assignment=placebo)
    except ObjectDoesNotExist:
        Product(assignment=placebo, formulation=formulation).save()


def update_supplier():
    try:
        Supplier.objects.get(name="merck")
    except ObjectDoesNotExist:
        Supplier(name="merck").save()


def update_labels():
    try:
        default = LabelSpecification.objects.get(name="default")
    except ObjectDoesNotExist:
        default = LabelSpecification().save()

    for name, label_config in site_label_configs.registry.items():
        LabelConfiguration.objects.create(name=name, label_specification=default)
    for label_configuration in LabelConfiguration.objects.filter(name__contains="patient"):
        label_configuration.requires_allocation = True
        label_configuration.save()


__all__ = ["update_initial_pharmacy_data"]
