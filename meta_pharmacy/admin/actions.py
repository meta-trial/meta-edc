import random
import string

import pandas as pd
from django.contrib import messages
from django.http import FileResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django_pandas.io import read_frame
from django_pylabels.models import LabelSpecification
from edc_pdutils.dataframes import get_subject_visit
from edc_sites.site import sites
from edc_utils import get_utcnow
from pylabels import Sheet, Specification

from meta_consent.models import SubjectConsent
from meta_rando.models import RandomizationList

from ..labels import LabelData as LabelDataCls
from ..labels import draw_label_with_code39
from ..models import LabelData

random.seed(7825541)


def print_test_label_sheet(modeladmin, request, queryset):
    if queryset.count() > 1 or queryset.count() == 0:
        messages.add_message(
            request,
            messages.ERROR,
            _("Select one and only one existing label specification"),
        )
    else:
        obj = queryset.first()
        specs = Specification(**obj.as_dict)
        sheet = Sheet(specs, draw_label_with_code39, border=obj.border)
        sheet.add_labels([LabelDataCls() for i in range(0, obj.rows * obj.columns)])
        buffer = sheet.save_to_buffer()

        return FileResponse(buffer, as_attachment=True, filename=f"test_print_{obj.name}.pdf")


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


def prepare_label_data(modeladmin, request, queryset):
    if queryset.count() > 1 or queryset.count() == 0:
        messages.add_message(
            request,
            messages.ERROR,
            _("Select one and only one existing label specification"),
        )
    else:
        obj = queryset.first()
        assignment = obj.lot_number.assignment
        now = get_utcnow()
        df = get_subject_visit(model="meta_subject.subjectvisit")
        df["last_visit_datetime"] = df["last_visit_datetime"].dt.normalize()
        df = df[
            (df.visit_code == df.last_visit_code)
            & (df.visit_code_sequence == 0)
            & (df.last_visit_datetime <= pd.to_datetime("today"))
            & (df.site_id == obj.site_id)
        ]
        df = df.reset_index()
        df_rando = read_frame(
            RandomizationList.objects.filter(assignment=assignment), verbose=False
        )
        df = df.merge(
            df_rando[["subject_identifier", "sid"]], on="subject_identifier", how="left"
        )
        df = df[df.sid.notna()]
        df_consent = read_frame(SubjectConsent.objects.filter(site=obj.site), verbose=False)
        df = df.merge(
            df_consent[["subject_identifier", "gender"]], on="subject_identifier", how="left"
        )
        df = df.reset_index()

        df["site_name"] = df["site_id"].apply(lambda x: sites.get(x).name)
        data = [
            LabelData(
                subject_identifier=row["subject_identifier"],
                label_batch=obj,
                gender=row["gender"],
                site_id=row["site_id"],
                site_name=row["site_name"],
                sid=row["sid"],
                reference="".join(  # nosec B311
                    random.choices(
                        string.ascii_letters.upper() + "0123456789", k=6
                    )  # nosec B311
                ),
                created=now,
            )
            for _, row in df.iterrows()
        ]
        created = len(LabelData.objects.bulk_create(data))
        url = reverse("meta_pharmacy_admin:meta_pharmacy_labeldata_changelist")
        url = f"{url}?q={obj.batch}"
        msg = format_html(
            _("Created batch %(batch)s with %(created)s records")
            % {
                "created": created,
                "batch": obj.batch,
                "url": url,
            }
        )
        messages.add_message(request, messages.SUCCESS, message=msg)
