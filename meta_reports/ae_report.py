from edc_adverse_event.pdf_reports import AePdfReport as BaseAePdfReport


class AePdfReport(BaseAePdfReport):
    weight_model = "meta_subject.followup"
