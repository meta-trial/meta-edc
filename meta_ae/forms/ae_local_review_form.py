from django import forms

from ..models import AeLocalReview
from .modelform_mixins import AeReviewModelFormMixin


class AeLocalReviewForm(AeReviewModelFormMixin, forms.ModelForm):
    class Meta(AeReviewModelFormMixin.Meta):
        model = AeLocalReview
        fields = "__all__"
