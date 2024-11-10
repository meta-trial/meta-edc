from edc_pharmacy.models import Rx, Stock
from edc_pharmacy.utils import format_qty
from edc_sites.site import sites as site_sites
from reportlab.graphics.shapes import Drawing, String


def draw_label_for_subject_with_barcode(
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
        rx = Rx.objects.get(registered_subject__subject_identifier=obj.subject_identifier)
    except Rx.DoesNotExist:
        site = "Amana Hospital"
    else:
        site = site_sites.get(rx.site.id).name

    br = barcode_cls(**barcode_opts)
    br.value = obj.code
    br.x = width - 110
    br.y = 30
    label.add(br)
    label.add(String(15, height - 20, "META III Study", fontSize=12))
    label.add(String(width - 100, height - 36, site.title(), fontSize=12))

    label.add(
        String(
            width - 100,
            height - 20,
            f"{obj.subject_identifier or "999-99-99999-9"}",
            fontSize=12,
        )
    )
    label.add(String(15, height - 40, "Dawa kwa ajili ya utafiti", fontSize=10))
    label.add(String(15, height - 52, "wa META III.", fontSize=10))
    label.add(String(15, height - 64, "Meza vidonge vinne usiku tu.", fontSize=10))
    qty = format_qty(obj.container.qty, obj.container)
    label.add(String(15, height - 88, f"{qty} tabs", fontSize=10))
    return label
