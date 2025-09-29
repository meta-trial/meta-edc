from edc_adverse_event.view_mixins import AeListboardViewMixin
from reportlab.lib.units import cm

from meta_reports.ae_report import AePdfReport


class CustomAeReport(AePdfReport):
    logo_data = {  # noqa: RUF012
        "app_label": "meta_edc",
        "filename": "meta_logo.png",
        "first_page": (4.0 * cm, 0.83 * cm),
        "later_pages": (3.0 * cm, 0.625 * cm),
    }


class AeListboardView(AeListboardViewMixin):
    pdf_report_cls = CustomAeReport
