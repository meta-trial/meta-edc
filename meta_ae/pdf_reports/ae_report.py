from edc_adverse_event.pdf_reports import AeReport as BaseAeReport

from .meta_pdf_report_mixin import MetaCrfReportMixin


class AeReport(MetaCrfReportMixin, BaseAeReport):

    pass
