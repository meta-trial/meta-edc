from edc_adverse_event.pdf_reports import DeathReport as BaseDeathReport

from .meta_pdf_report_mixin import MetaCrfReportMixin


class DeathReport(MetaCrfReportMixin, BaseDeathReport):

    pass
