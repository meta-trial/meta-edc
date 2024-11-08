from django.contrib.sites.models import Site
from edc_constants.constants import FEMALE
from edc_pharmacy.models import Container, ContainerType
from edc_pharmacy.models import StockRequestItem as BaseStockRequestItem


class StockRequestItem(BaseStockRequestItem):

    @property
    def test_data(self):
        container_type = ContainerType(name="bottle")
        return dict(
            container=Container(name="bottle of 128", container_type=container_type, qty=128),
            subject_identifier="999-99999-9",
            gender=FEMALE,
            sid=9999,
            site=Site.objects.all()[0],
        )

    class Meta:
        proxy = True
        verbose_name = "Stock Request item"
        verbose_name_plural = "Stock Request items"
