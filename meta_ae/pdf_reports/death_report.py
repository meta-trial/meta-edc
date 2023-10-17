from edc_adverse_event.pdf_reports import DeathPdfReport as BaseDeathPdfReport

from .meta_pdf_report_mixin import MetaCrfReportMixin


class DeathReport(MetaCrfReportMixin, BaseDeathPdfReport):
    pass
