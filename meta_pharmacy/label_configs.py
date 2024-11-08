from edc_pharmacy.labels import draw_stock_label_code39
from edc_pylabels.site_label_configs import site_label_configs

from .labels import draw_label_for_subject_with_code39, draw_label_with_code39_test_data

site_label_configs.register(
    "meta3_label_config",
    draw_label_for_subject_with_code39,
    "edc_pharmacy.stockrequestitem",
    test_data_func=draw_label_with_code39_test_data,
)

site_label_configs.register(
    "stock_label_config",
    draw_stock_label_code39,
    "edc_pharmacy.stock",
    test_data_func=draw_label_with_code39_test_data,
)
