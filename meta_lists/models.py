from edc_list_data.model_mixins import ListModelMixin


class Symptoms(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Symptoms"
        verbose_name_plural = "Symptoms"


class ArvRegimens(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "ARV Regimens"
        verbose_name_plural = "ARV Regimens"


class OffstudyReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Offstudy Reasons"
        verbose_name_plural = "Offstudy Reasons"


class OiProphylaxis(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "OI Prophylaxis"
        verbose_name_plural = "OI Prophylaxis"


class BaselineSymptoms(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Baseline Symptoms"
        verbose_name_plural = "Baseline Symptoms"


class DiabetesSymptoms(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Diabetes Symptoms"
        verbose_name_plural = "Diabetes Symptoms"


class HypertensionMedications(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Hypertension Medications"
        verbose_name_plural = "Hypertension Medications"


class NonAdherenceReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Non-Adherence Reasons"
        verbose_name_plural = "Non-Adherence Reasons"
