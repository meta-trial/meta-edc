from edc_adverse_event.pdf_reports import AePdfReport as BaseAePdfReport

from .meta_pdf_report_mixin import MetaCrfReportMixin


class AePdfReport(MetaCrfReportMixin, BaseAePdfReport):
    pass
