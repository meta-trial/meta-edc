from django import forms
from django.utils.translation import gettext as _

from ..models import LabelBatchBarcodes, LabelData


class LabelBatchBarcodesForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("barcodes"):
            barcodes = cleaned_data["barcodes"].split()
            if len(barcodes) != len(list(set(barcodes))):
                raise forms.ValidationError(
                    {"barcodes": "The list of barcodes must be unique."}
                )
            if (
                cleaned_data.get("bottle_count") is None
                or cleaned_data.get("bottle_count") == 0
            ):
                raise forms.ValidationError(
                    {"bottle_count": "Expected the number of bottles prepared"}
                )
            if len(barcodes) != cleaned_data.get("bottle_count"):
                raise forms.ValidationError(
                    "Counts do not match. The bottle count should match the "
                    "number of barcodes scanned."
                )
            qs_label_data = LabelData.objects.filter(label_batch=self.instance.label_batch)
            if qs_label_data.filter(reference__in=barcodes).count() != len(barcodes):
                raise forms.ValidationError(
                    {
                        "barcodes": _(
                            "Invalid barcodes found. Not all barcodes belong to this batch."
                        )
                    }
                )

    class Meta:
        model = LabelBatchBarcodes
        fields = "__all__"
