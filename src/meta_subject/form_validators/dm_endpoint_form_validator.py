from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from edc_crf.crf_form_validator import CrfFormValidator
from edc_form_validators import INVALID_ERROR

from meta_reports.models import Endpoints
from meta_reports.tasks import update_endpoints_table


class DmEndpointFormValidator(CrfFormValidator):
    def clean(self):
        # recalc from endpoint report to confirm the endpoint has been reached
        update_endpoints_table(subject_identifiers=[self.subject_identifier])
        try:
            Endpoints.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            url = reverse("meta_reports_admin:meta_reports_glucosesummary_changelist")
            link = render_to_string(
                "meta_reports/columns/subject_identifier_column.html",
                {
                    "subject_identifier": self.subject_identifier,
                    "url": url,
                    "label": "Glucose Summary",
                },
            )
            self.raise_validation_error(
                {
                    "__all__": format_html(
                        "Subject has not reached the protocol endpoint. See {link}",
                        link=mark_safe(link),  # noqa: S308
                    )
                },
                INVALID_ERROR,
            )
