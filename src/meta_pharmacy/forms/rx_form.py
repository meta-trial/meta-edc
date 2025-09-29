from django import forms

from ..models import Rx


class RxForm(forms.ModelForm):
    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = Rx
        fields = "__all__"
