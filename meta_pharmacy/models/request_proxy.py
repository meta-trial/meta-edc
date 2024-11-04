from edc_pharmacy.models import Request as BaseRequest


class Request(BaseRequest):
    class Meta:
        proxy = True
        verbose_name = "Request"
        verbose_name_plural = "Requests"
