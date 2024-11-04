from edc_pylabels.site_label_configs import site_label_configs

from .labels import draw_label_with_code39, draw_label_with_code39_test_data

site_label_configs.register(
    "meta3_label_config",
    draw_label_with_code39,
    "edc_pharmacy.requestitem",
    test_data_func=draw_label_with_code39_test_data,
)
