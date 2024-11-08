from edc_pharmacy.models import Rx, Stock
from edc_pharmacy.utils import format_qty
from edc_sites.site import sites as site_sites
from reportlab.graphics.barcode.widgets import BarcodeStandard39
from reportlab.graphics.charts.textlabels import Label as RlLabel
from reportlab.graphics.shapes import Drawing, String


def draw_label_for_subject_with_code39(
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
        gender = "?"
        site = "NOSITE"
        sid = "00000"
    else:
        gender = rx.registered_subject.gender
        site = site_sites.get(rx.site.id).name
        sid = rx.rando_sid

    br = BarcodeStandard39(
        humanReadable=True, checksum=False, barHeight=30, barWidth=0.7, gap=1.7
    )
    br.value = obj.code
    br.x = width - 140
    br.y = 25
    label.add(br)
    label.add(String(15, height - 20, f"META III Study - {site.title()}", fontSize=10))
    label.add(
        String(
            width - 110,
            height - 40,
            f"{obj.subject_identifier or "SUBJECTID"}{gender}",
            fontSize=12,
        )
    )
    label.add(String(15, height - 40, "Dawa kwa ajili ya utafiti", fontSize=10))
    label.add(String(15, height - 50, "wa META III.", fontSize=10))
    label.add(String(15, height - 70, "Meza vidonge vinne usiku tu.", fontSize=10))
    qty = format_qty(obj.container.qty, obj.container)
    label.add(String(15, 20, f"{qty} tabs", fontSize=10))
    lab = RlLabel(x=width - 20, y=40, fontSize=10, angle=90)
    lab.setText(str(sid))
    label.add(lab)
    return label
