from django.contrib.admin import AdminSite as DjangoAdminSite
from edc_locator.models import SubjectLocator

from meta_consent.models import SubjectConsent
from meta_screening.models import SubjectScreening
from meta_subject.models import SubjectRequisition, SubjectVisit


class AdminSite(DjangoAdminSite):
    site_title = "Ambition Subject"
    site_header = "Ambition Subject"
    index_title = "Ambition Subject"
    site_url = "/administration/"


meta_test_admin = AdminSite(name="meta_test_admin")

meta_test_admin.register(SubjectScreening)
meta_test_admin.register(SubjectConsent)
meta_test_admin.register(SubjectLocator)
meta_test_admin.register(SubjectVisit)
meta_test_admin.register(SubjectRequisition)
