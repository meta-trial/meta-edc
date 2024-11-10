from reportlab.graphics.barcode.widgets import BarcodeCode128
from reportlab.graphics.shapes import Drawing

from .draw_label_for_subject_with_barcode import draw_label_for_subject_with_barcode


def draw_label_for_subject_with_code128(*args) -> Drawing:
    barcode_opts = dict(
        humanReadable=True,
        barHeight=30,
        barWidth=0.7,
        gap=1.7,
    )
    return draw_label_for_subject_with_barcode(BarcodeCode128, barcode_opts, *args)
