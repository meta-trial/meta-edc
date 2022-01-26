import sys

from django.apps import AppConfig as DjangoAppConfig
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_migrate
from django_extensions.management.color import color_style

from meta_edc.meta_version import PHASE_THREE, get_meta_version

style = color_style()


def post_migrate_populate_pharmacy_models(sender=None, **kwargs):  # noqa
    """Create or update pharmacy static models."""
    from django.apps import apps as django_apps

    if get_meta_version() == PHASE_THREE:
        sys.stdout.write(
            style.MIGRATE_HEADING("Populating static pharmacy models for META3:\n")
        )

        medication_model_cls = django_apps.get_model("edc_pharmacy.medication")
        formulation_model_cls = django_apps.get_model("edc_pharmacy.formulation")
        dosage_guideline_model_cls = django_apps.get_model(
            "edc_pharmacy.dosageguideline"
        )
        route_model_cls = django_apps.get_model("edc_pharmacy.route")
        units_model_cls = django_apps.get_model("edc_pharmacy.units")
        formulation_type_model_cls = django_apps.get_model(
            "edc_pharmacy.formulationtype"
        )
        frequency_units_model_cls = django_apps.get_model("edc_pharmacy.frequencyunits")

        units = units_model_cls.objects.get(name="mg")
        formulation_type = formulation_type_model_cls.objects.get(name="tablet")
        route = route_model_cls.objects.get(name="oral")
        frequency_units = frequency_units_model_cls.objects.get(name="day")

        # medication

        try:
            medication_obj = medication_model_cls.objects.get(name="metformin")
        except ObjectDoesNotExist as e:
            medication_obj = medication_model_cls.objects.create(
                name="metformin", display_name="Metformin"
            )
        else:
            medication_obj.display_name = "Metformin"
            medication_obj.save()

        # formulation
        try:
            formulation_obj = formulation_model_cls.objects.get(
                medication=medication_obj, strength=500, units=units
            )
        except ObjectDoesNotExist as e:
            formulation_model_cls.objects.create(
                medication=medication_obj,
                strength=500,
                units=units,
                formulation_type=formulation_type,
                route=route,
            )
        else:
            formulation_obj.strength = 500
            formulation_obj.units = units
            formulation_obj.formulation_type = formulation_type
            formulation_obj.route = route
            formulation_obj.save()

        # dosage guideline
        for dose in [1000, 2000]:
            try:
                dosage_guideline = dosage_guideline_model_cls.objects.get(
                    medication=medication_obj, dose=dose, dose_units=units
                )
            except ObjectDoesNotExist as e:
                dosage_guideline_model_cls.objects.create(
                    medication=medication_obj,
                    dose=dose,
                    dose_units=units,
                    frequency=1,
                    frequency_units=frequency_units,
                )
            else:
                dosage_guideline.medication = medication_obj
                dosage_guideline.dose = dose
                dosage_guideline.dose_units = units
                dosage_guideline.frequency = 1
                dosage_guideline.frequency_units = frequency_units
                dosage_guideline.save()


class AppConfig(DjangoAppConfig):
    name = "meta_pharmacy"
    verbose_name = f"META{get_meta_version()}: Pharmacy"

    def ready(self):
        post_migrate.connect(post_migrate_populate_pharmacy_models, sender=self)
