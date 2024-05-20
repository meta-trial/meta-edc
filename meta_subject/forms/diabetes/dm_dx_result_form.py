from django import forms

from ...models import DmDxResult


class DmDxResultForm(forms.ModelForm):
    # form_validator_cls = DmDxResultFormValidator

    class Meta:
        model = DmDxResult
        fields = "__all__"
