from edc_pharmacy.labels import draw_label_watermark
from edc_pharmacy.models import Stock
from edc_pharmacy.utils import format_qty
from edc_sites.site import sites as site_sites
from reportlab.graphics.shapes import Drawing, Group, String
from reportlab.pdfbase.pdfmetrics import stringWidth


def draw_label_for_subject_with_barcode(  # noqa: PLR0913
    barcode_cls,
    barcode_opts: dict,
    label: Drawing,
    width: int | float,
    height: int | float,
    obj: Stock,
) -> Drawing:
    """Callable to draw a single study medication label given a model
    instance `obj`
    """
    try:
        single_site = site_sites.get(
            obj.allocation.stock_request_item.stock_request.location.site.id
        )
    except AttributeError:
        label.add(String(15, height - 20, "Error: Unable to generate label", fontSize=10))
        label.add(String(15, height - 40, str(obj.code), fontSize=10))
        label.add(String(15, height - 60, str(obj.location), fontSize=10))
    else:
        draw_label_watermark(label, width, height, fontSize=18)

        br = barcode_cls(**barcode_opts)
        br.value = obj.code
        br.x = width - 110
        br.y = 40
        label.add(br)

        label.add(String(15, height - 35, single_site.title, fontSize=10))

        label.add(String(15, height - 20, "META III Study", fontSize=12))
        label.add(String(15, height - 55, "Dawa kwa ajili ya utafiti", fontSize=10))
        label.add(String(15, height - 67, "wa META III.", fontSize=10))
        label.add(String(15, height - 79, "Meza vidonge vinne usiku tu.", fontSize=10))

        text_group = Group()
        subject_identifier = (
            obj.allocation.registered_subject.subject_identifier or "999-99-99999-9"
        )
        text_width = stringWidth(subject_identifier, "Helvetica", 12)
        text_string = String(
            width - text_width - 10, height - 20, subject_identifier, fontSize=12
        )
        text_group.add(text_string)

        qty_text = f"{format_qty(obj.container.qty, obj.container)} tabs"
        text_width = stringWidth(qty_text, "Helvetica", 10)
        text_string = String(width - text_width - 10, height - 95, qty_text, fontSize=10)
        text_group.add(text_string)

        label.add(text_group)

    return label
