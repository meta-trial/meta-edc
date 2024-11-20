import random

from django.contrib import messages
from django.http import FileResponse
from django.utils.translation import gettext as _
from django_pylabels.models import LabelSpecification
from edc_utils import get_utcnow
from pylabels import Sheet, Specification

from ..labels import draw_label_with_code39
from ..models import LabelData

random.seed(7825541)


def print_label_sheet(modeladmin, request, queryset):
    label_data = [obj for obj in queryset]
    obj = LabelSpecification.objects.get(name="meta3")
    specs = Specification(**obj.as_dict)
    sheet = Sheet(specs, draw_label_with_code39, border=obj.border)
    sheet.add_labels(label_data)
    buffer = sheet.save_to_buffer()
    now = get_utcnow()
    queryset.update(printed=True, printed_datetime=now)
    return FileResponse(
        buffer, as_attachment=True, filename=f"{obj.name}_{now.strftime("%Y-%m-%d %H:%M")}.pdf"
    )


def print_label_sheet_from_batch(modeladmin, request, queryset):
    if queryset.count() > 1 or queryset.count() == 0:
        messages.add_message(
            request,
            messages.ERROR,
            _("Select one and only one existing label specification"),
        )
    queryset = LabelData.objects.filter(label_batch=queryset.first())
    return print_label_sheet(modeladmin, request, queryset)
