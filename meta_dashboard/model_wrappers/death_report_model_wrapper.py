from edc_model_wrapper import ModelWrapper


class DeathReportModelWrapper(ModelWrapper):
    next_url_name = "subject_listboard_url"
    model = "meta_ae.deathreport"
    next_url_attrs = ["subject_identifier"]

    @property
    def pk(self):
        return str(self.object.pk)

    @property
    def subject_identifier(self):
        return self.object.subject_identifier
