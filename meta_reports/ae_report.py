from edc_adverse_event.pdf_reports import AeReport as BaseAeReport


class AeReport(BaseAeReport):

    weight_model = "meta_subject.followup"
