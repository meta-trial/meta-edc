# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from edc_utils import get_utcnow

# from .batch_barcodes import BatchBarcodes
# from .label_data import LabelData
# from .stock_transfer import StockTransfer

# @receiver(post_save, weak=False, sender=Batch,
#     dispatch_uid="update_user_profile_on_post_save")
# def update_label_data_on_post_save(sender, instance, raw, **kwargs):
#     if not raw:
#         barcodes = []
#         for obj in BatchBarcodes.objects.filter(label_batch=instance):
#             barcodes.extend(obj.barcodes.split())
#         if barcodes:
#             LabelData.objects.filter(
#                 label_batch=instance, reference__in=barcodes).update(
#                 scanned=True, scanned_datetime=get_utcnow()
#             )
