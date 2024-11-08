from edc_pharmacy.models import StockRequest as BaseStockRequest


class StockRequest(BaseStockRequest):
    class Meta:
        proxy = True
        verbose_name = "Stock request"
        verbose_name_plural = "Stock requests"
