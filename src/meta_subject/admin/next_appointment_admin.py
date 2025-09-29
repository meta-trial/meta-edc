from __future__ import annotations

from django.contrib import admin
from edc_appointment.modeladmin_mixins import NextAppointmentCrfModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import NextAppointmentForm
from ..models import NextAppointment
from .modeladmin import CrfModelAdminMixin

__all__ = ["NextAppointmentAdmin"]


@admin.register(NextAppointment, site=meta_subject_admin)
class NextAppointmentAdmin(
    CrfModelAdminMixin, NextAppointmentCrfModelAdminMixin, SimpleHistoryAdmin
):
    form = NextAppointmentForm
