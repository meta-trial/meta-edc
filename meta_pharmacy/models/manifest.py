# from django.db import models
# from django.db.models import PROTECT
# from edc_constants.constants import NOT_APPLICABLE, OTHER
# from edc_model.models import BaseUuidModel, HistoricalRecords
# from edc_pharmacy.models import Formulation, Order, Product
# from edc_randomization.constants import ACTIVE, PLACEBO
#
#
# class Manifest(BaseUuidModel):
#
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#
#     invoice_date = models.DateField()
#
#     lot = models.CharField(max_length=25, unique=True)
#
#     product = models.ForeignKey(Product, on_delete=models.PROTECT)
#
#     formulation = models.ForeignKey(Formulation, on_delete=PROTECT, null=True, blank=False)
#
#     manufacture_date = models.DateField()
#
#     expiration_date = models.DateField()
#
#     assignment = models.CharField(
#         max_length=25,
#         choices=(
#             (ACTIVE, "Active"),
#             (PLACEBO, "Placebo"),
#             (OTHER, "Other"),
#             (NOT_APPLICABLE, "Not applicable"),
#         ),
#     )
#
#     qty = models.IntegerField(null=True)
#
#     objects = models.Manager()
#
#     history = HistoricalRecords()
#
#     def __str__(self):
#         return f"{self.formulation}-{self.assignment[0].upper()}: {self.lot}"
#
#     class Meta(BaseUuidModel.Meta):
#         verbose_name = "Lot"
#         verbose_name_plural = "Lots"
