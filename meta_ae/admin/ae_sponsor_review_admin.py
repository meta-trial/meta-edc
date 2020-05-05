from django.contrib import admin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import meta_ae_admin
from ..forms import AeLocalReviewForm
from ..models import AeLocalReview
from .modeladmin_mixins import AeReviewModelAdminMixin


@admin.register(AeLocalReview, site=meta_ae_admin)
class AeLocalReviewAdmin(AeReviewModelAdminMixin, SimpleHistoryAdmin):

    form = AeLocalReviewForm
