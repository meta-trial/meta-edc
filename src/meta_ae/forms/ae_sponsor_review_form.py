from django import forms

from ..models import AeSponsorReview
from .modelform_mixins import AeReviewModelFormMixin


class AeSponsorReviewForm(AeReviewModelFormMixin, forms.ModelForm):
    class Meta(AeReviewModelFormMixin.Meta):
        model = AeSponsorReview
        fields = "__all__"
