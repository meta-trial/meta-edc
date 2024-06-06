from django.contrib import admin
from edc_appointment.admin import AppointmentAdmin as BaseAdmin
from edc_appointment.admin_site import edc_appointment_admin
from edc_appointment.models import Appointment

from .list_filters import LastSeenDaysListFilter

edc_appointment_admin.unregister(Appointment)


@admin.register(Appointment, site=edc_appointment_admin)
class AppointmentAdmin(BaseAdmin):

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        list_filter = list(list_filter)
        list_filter.insert(6, LastSeenDaysListFilter)
        list_filter = tuple(list_filter)
        return list_filter
