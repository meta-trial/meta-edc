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
    """For a trial with just active and placebo.

    Better to get these labels from edc_randomizer.
    """
    for assignment in ["placebo", "active"]:
        try:
            Assignment.objects.get(name=assignment)
        except ObjectDoesNotExist:
            Assignment.objects.create(name=assignment, display_name=assignment.title())


def update_container():
    """Here we order a number of tablets. The manufacturer sends
    the order in large containers, barrels of about 30K tablets
    per barrel. We repack/decant into bottles of 128 tablets
    """
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
            display_name="Barrel 30K",
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
    """Base the locations on the sites in the trial plus
    a "central" pharmacy"""
    for obj in Location.objects.exclude(name="central"):
        obj.site_id = Site.objects.get(name=obj.name).id
        obj.save(update_fields=["site_id"])


def update_product():
    """Define the product, in this case just two; active and placebo.

    Formulation is defined before running this script.

    In this case the formulation is just the study drug/IMP.
    """
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
    """In this case MERCK"""
    try:
        Supplier.objects.get(name="merck")
    except ObjectDoesNotExist:
        Supplier(name="merck").save()


def update_labels():
    """The default label spec is a 2 x 6 label sheet

    Add "label congigs" as registered in the "site_label_configs"
    global. In this case there are three labels:
    * a bulk label for the barrels
    * a generic vertical label for decanted stock (bottles of 128)
    * a patient label for allocated stock (bottles of 128)

    The patient label will be placed over the generic vertical label
    once the stock item is allocated to a subject.
    """
    try:
        default = LabelSpecification.objects.get(name="default")
    except ObjectDoesNotExist:
        LabelSpecification().save()
        default = LabelSpecification.objects.get(name="default")

    for name in site_label_configs.registry:
        LabelConfiguration.objects.create(name=name, label_specification=default)
    for label_configuration in LabelConfiguration.objects.filter(name__contains="patient"):
        label_configuration.requires_allocation = True
        label_configuration.save()


__all__ = ["update_initial_pharmacy_data"]
