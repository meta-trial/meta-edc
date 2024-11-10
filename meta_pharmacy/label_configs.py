from edc_pharmacy.labels import (
    draw_bulk_stock_label_code128,
    draw_patient_stock_label_code128,
    draw_vertical_barcode_only_code128,
)
from edc_pylabels.site_label_configs import site_label_configs

from .labels import draw_label_with_test_data

# create a label class to pass instead of a model

site_label_configs.register(
    "vertical_stock_barcode_128",
    draw_vertical_barcode_only_code128,
    "edc_pharmacy.stock",
    test_data_func=draw_label_with_test_data,
)

site_label_configs.register(
    "bulk_stock_barcode_128",
    draw_bulk_stock_label_code128,
    "edc_pharmacy.stock",
    test_data_func=draw_label_with_test_data,
)

site_label_configs.register(
    "patient_barcode_128",
    draw_patient_stock_label_code128,
    "edc_pharmacy.stock",
    test_data_func=draw_label_with_test_data,
)
