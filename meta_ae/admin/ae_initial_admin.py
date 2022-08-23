from django.contrib import admin
from django.utils.html import format_html
from edc_adverse_event.modeladmin_mixins import AeInitialModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_notification.utils import get_email_contacts

from ..admin_site import meta_ae_admin
from ..forms import AeInitialForm
from ..models import AeInitial


@admin.register(AeInitial, site=meta_ae_admin)
class AeInitialAdmin(AeInitialModelAdminMixin, SimpleHistoryAdmin):

    form = AeInitialForm
    email_contact = get_email_contacts("ae_reports")
    additional_instructions = format_html(
        "Complete the initial AE report and forward to the TMG. "
        'Email to <a href="mailto:{}">{}</a>',
        email_contact,
        email_contact,
    )
