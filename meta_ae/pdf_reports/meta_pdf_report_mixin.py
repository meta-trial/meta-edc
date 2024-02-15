from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist


class MetaCrfReportMixin:
    weight_model = "meta_subject.followup"

    @property
    def unblinded(self):
        unblinding_request_model_cls = django_apps.get_model(
            "edc_unblinding.unblindingrequest"
        )
        try:
            unblinded = unblinding_request_model_cls.objects.get(
                subject_identifier=self.subject_identifier, approved=True
            )
        except ObjectDoesNotExist:
            unblinded = False
        return unblinded
