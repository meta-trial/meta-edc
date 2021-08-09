import pdb
import sys
from copy import deepcopy
from unittest import skipIf

from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from django.test import tag
from django.test.utils import override_settings
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_extensions.management.color import color_style
from django_webtest import WebTest
from edc_appointment.constants import IN_PROGRESS_APPT, SCHEDULED_APPT
from edc_appointment.models import Appointment
from edc_auth import AE, AUDITOR, CLINIC, EVERYONE, EXPORT, LAB, PII, SCREENING, TMG
from edc_constants.constants import YES
from edc_dashboard.url_names import url_names
from edc_randomization.admin import register_admin
from edc_randomization.site_randomizers import site_randomizers
from edc_sites import add_or_update_django_sites
from edc_test_utils.webtest import login
from edc_utils import get_utcnow
from model_bakery import baker
from webtest.app import AppError

from meta_edc.meta_version import get_meta_version
from meta_rando.randomizers import RandomizerPhaseThree, RandomizerPhaseTwo
from meta_screening.models import ScreeningPartOne, ScreeningPartThree, ScreeningPartTwo
from meta_screening.models.subject_screening import SubjectScreening
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_screening.tests.options import (
    get_part_one_eligible_options,
    get_part_three_eligible_options,
    get_part_two_eligible_options,
)
from meta_sites.sites import all_sites

style = color_style()
User = get_user_model()

app_prefix = "meta"
screening_listboard_url = f"{app_prefix}_dashboard:screening_listboard_url"


@override_settings(SIMPLE_HISTORY_PERMISSIONS_ENABLED=True)
class AdminSiteTest(MetaTestCaseMixin, WebTest):
    def setUp(self):
        self.user = User.objects.create_superuser("user_login", "u@example.com", "pass")

    def login(self, **kwargs):
        return login(self, redirect_url="home_url", **kwargs)

    @tag("webtest")
    def test_login(self):
        self.login(superuser=False, groups=[EVERYONE, AUDITOR])

    @tag("webtest")
    def test_ae(self):
        self.login(superuser=False, groups=[EVERYONE, AUDITOR])
        response = self.app.get(reverse("meta_ae:home_url"), user=self.user, status=302)
        response = response.follow()
        self.assertIn(f"META{get_meta_version()}: Adverse Events", response)
        self.app.get(
            reverse("edc_adverse_event:ae_home_url"), user=self.user, status=200
        )
        self.app.get(
            reverse("edc_adverse_event:tmg_home_url"), user=self.user, status=200
        )
        self.app.get(reverse("edc_data_manager:home_url"), user=self.user, status=302)

    @tag("webtest")
    def test_home_everyone(self):
        self.login(superuser=False, groups=[EVERYONE])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertNotIn("Screening", response)
        self.assertNotIn("Subjects", response)
        self.assertNotIn("Specimens", response)
        self.assertNotIn("Adverse events", response)
        self.assertNotIn("Pharmacy", response)
        self.assertNotIn("Action items", response)
        self.assertNotIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

    @tag("webtest")
    def test_home_auditor(self):
        self.login(superuser=False, groups=[EVERYONE, AUDITOR])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertIn("Screening", response)
        self.assertIn("Subjects", response)
        self.assertIn("Specimens", response)
        self.assertIn("Adverse events", response)
        self.assertIn("TMG Reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertIn("Action items", response)
        self.assertNotIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

        response = response.click(linkid="home_list_group_aetmg")
        self.assertIn("TMG Reports", response)

    @tag("webtest")
    def test_home_clinic(self):
        self.login(superuser=False, groups=[EVERYONE, CLINIC, AE, PII, LAB])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertIn("Screening", response)
        self.assertIn("Subjects", response)
        self.assertIn("Specimens", response)
        self.assertIn("Adverse events", response)
        self.assertNotIn("TMG Reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertIn("Action items", response)
        self.assertNotIn("Export data", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

    @tag("webtest")
    def test_home_export(self):
        self.login(superuser=False, groups=[EVERYONE, EXPORT])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertNotIn("Screening", response)
        self.assertNotIn("Subjects", response)
        self.assertNotIn("Specimens", response)
        self.assertNotIn("Adverse events", response)
        self.assertNotIn("TMG Reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertNotIn("Action items", response)
        self.assertIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

    @tag("webtest")
    def test_home_tmg(self):
        self.login(superuser=False, groups=[EVERYONE, TMG])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertIn("Screening", response)
        self.assertIn("Subjects", response)
        self.assertNotIn("Specimens", response)
        self.assertIn("Adverse events", response)
        self.assertIn("TMG Reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertIn("Action items", response)
        self.assertNotIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)
        response = response.click(linkid="home_list_group_aetmg")
        self.assertIn("TMG Reports", response)

    @tag("webtest")
    def test_home_lab(self):
        self.login(superuser=False, groups=[EVERYONE, LAB])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertIn("Screening", response)
        self.assertIn("Subjects", response)
        self.assertIn("Specimens", response)
        self.assertNotIn("Adverse events", response)
        self.assertNotIn("TMG Reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertNotIn("Action items", response)
        self.assertNotIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

    @skipIf(get_meta_version() != 2, "not version 2")
    @tag("webtest")
    # @override_settings(META_PHASE=2)
    def test_screening_form_phase2(self):
        site_randomizers._registry = {}
        site_randomizers.loaded = False
        site_randomizers.register(RandomizerPhaseTwo)
        register_admin()

        part_one_data = deepcopy(get_part_one_eligible_options())
        report_datetime = part_one_data.get("report_datetime")
        part_one_data.update(
            dict(
                report_datetime_0=report_datetime.strftime("%Y-%m-%d"),
                report_datetime_1=report_datetime.strftime("%H:%M"),
                continue_part_two=YES,
            )
        )
        (
            home_page,
            add_screening_part_two,
            screening_identifier,
        ) = self.webtest_for_screening_form_part_one(part_one_data)

        part_two_data = deepcopy(get_part_two_eligible_options())
        report_datetime = part_two_data.get("part_two_report_datetime")
        appt_datetime = part_two_data.get("appt_datetime")
        part_two_data.update(
            dict(
                part_two_report_datetime_0=report_datetime.strftime("%Y-%m-%d"),
                part_two_report_datetime_1=report_datetime.strftime("%H:%M"),
                appt_datetime_0=appt_datetime.strftime("%Y-%m-%d"),
                appt_datetime_1=appt_datetime.strftime("%H:%M"),
            )
        )
        (
            home_page,
            add_screening_part_three,
            screening_identifier,
        ) = self.webtest_for_screening_form_part_two(
            home_page, add_screening_part_two, screening_identifier, part_two_data
        )

        part_three_data = deepcopy(get_part_three_eligible_options())
        report_datetime = part_three_data.get("part_three_report_datetime")
        ifg_datetime = part_three_data.get("ifg_datetime")
        ogtt_datetime = part_three_data.get("ogtt_datetime")
        part_three_data = deepcopy(part_three_data)
        part_three_data.update(
            dict(
                part_three_report_datetime_0=report_datetime.strftime("%Y-%m-%d"),
                part_three_report_datetime_1=report_datetime.strftime("%H:%M"),
                ifg_datetime_0=ifg_datetime.strftime("%Y-%m-%d"),
                ifg_datetime_1=ifg_datetime.strftime("%H:%M"),
                ogtt_datetime_0=ogtt_datetime.strftime("%Y-%m-%d"),
                ogtt_datetime_1=ogtt_datetime.strftime("%H:%M"),
            )
        )
        (
            screening_listboard_page,
            screening_identifier,
        ) = self.webtest_for_screening_form_part_three(
            home_page, add_screening_part_three, screening_identifier, part_three_data
        )
        self.assertIn(screening_identifier, screening_listboard_page)
        self.assertIn("Consent", screening_listboard_page)

    @skipIf(get_meta_version() != 3, "not version 3")
    @tag("webtest")
    def test_screening_form_phase3(self):
        site_randomizers._registry = {}
        site_randomizers.loaded = False
        site_randomizers.register(RandomizerPhaseThree)
        register_admin()

        part_one_data = deepcopy(get_part_one_eligible_options())
        report_datetime = part_one_data.get("report_datetime")
        part_one_data.update(
            dict(
                report_datetime_0=report_datetime.strftime("%Y-%m-%d"),
                report_datetime_1=report_datetime.strftime("%H:%M"),
                continue_part_two=YES,
            )
        )
        (
            home_page,
            add_screening_part_two,
            screening_identifier,
        ) = self.webtest_for_screening_form_part_one(part_one_data)
        part_two_data = deepcopy(get_part_two_eligible_options())
        report_datetime = part_two_data.get("part_two_report_datetime")
        appt_datetime = part_two_data.get("appt_datetime")
        part_two_data.update(
            dict(
                part_two_report_datetime_0=report_datetime.strftime("%Y-%m-%d"),
                part_two_report_datetime_1=report_datetime.strftime("%H:%M"),
                appt_datetime_0=appt_datetime.strftime("%Y-%m-%d"),
                appt_datetime_1=appt_datetime.strftime("%H:%M"),
            )
        )
        (
            home_page,
            add_screening_part_three,
            screening_identifier,
        ) = self.webtest_for_screening_form_part_two(
            home_page, add_screening_part_two, screening_identifier, part_two_data
        )

        part_three_data = deepcopy(get_part_three_eligible_options())
        report_datetime = part_three_data.get("part_three_report_datetime")
        ifg_datetime = part_three_data.get("ifg_datetime")
        ogtt_datetime = part_three_data.get("ogtt_datetime")
        part_three_data.update(
            dict(
                part_three_report_datetime_0=report_datetime.strftime("%Y-%m-%d"),
                part_three_report_datetime_1=report_datetime.strftime("%H:%M"),
                ifg_datetime_0=ifg_datetime.strftime("%Y-%m-%d"),
                ifg_datetime_1=ifg_datetime.strftime("%H:%M"),
                ogtt_datetime_0=ogtt_datetime.strftime("%Y-%m-%d"),
                ogtt_datetime_1=ogtt_datetime.strftime("%H:%M"),
            )
        )
        (
            screening_listboard_page,
            screening_identifier,
        ) = self.webtest_for_screening_form_part_three(
            home_page, add_screening_part_three, screening_identifier, part_three_data
        )
        self.assertIn(screening_identifier, screening_listboard_page)
        self.assertIn("Consent", screening_listboard_page)

    def webtest_for_screening_form_part_one(self, part_one_data):
        self.login(superuser=False, groups=[EVERYONE, SCREENING, CLINIC, PII])
        home_page = self.app.get(reverse("home_url"), user=self.user, status=200)
        screening_listboard_page = home_page.click(description="Screening", index=1)
        add_screening_page = screening_listboard_page.click(
            description="Add Subject Screening"
        )
        # submit blank form
        response = add_screening_page.form.submit()
        self.assertIn("Please correct the errors below", response)
        # submit completed form
        for field, _ in add_screening_page.form.fields.items():
            try:
                add_screening_page.form[field] = part_one_data[field]
            except KeyError:
                print(field)
        page = add_screening_page.form.submit()
        soup = BeautifulSoup(page.content, "html.parser")
        errorlist = soup.find_all("ul", "errorlist")
        self.assertEqual([], errorlist)

        # redirects back to listboard
        url = reverse(screening_listboard_url)
        self.assertRedirects(page, url)

        # new screened subject is available
        obj = SubjectScreening.objects.all().last()
        screening_listboard_page = home_page.click(description="Screening", index=1)
        self.assertIn(obj.screening_identifier, screening_listboard_page)

        # shows P1 | P2 | P3 | PENDING
        self.assertIn("PENDING", screening_listboard_page)
        add_screening_part_two = screening_listboard_page.click(
            description="P2", index=0
        )
        self.assertEqual(add_screening_part_two.status_code, 200)
        return home_page, add_screening_part_two, obj.screening_identifier

    def webtest_for_screening_form_part_two(
        self, home_page, add_screening_part_two, screening_identifier, part_two_data
    ):
        # submit completed form
        for field, _ in add_screening_part_two.form.fields.items():
            try:
                add_screening_part_two.form[field] = part_two_data[field]
            except KeyError:
                print(field)
        page = add_screening_part_two.form.submit()
        soup = BeautifulSoup(page.content, "html.parser")
        errorlist = soup.find_all("ul", "errorlist")
        self.assertEqual([], errorlist)
        # redirects back to listboard
        obj = SubjectScreening.objects.all().last()
        url = reverse(screening_listboard_url, args=(obj.screening_identifier,))
        self.assertRedirects(page, url)
        # shows P1 | P2 | P3 | PENDING
        screening_listboard_page = home_page.click(description="Screening", index=1)
        self.assertIn("PENDING", screening_listboard_page)
        add_screening_part_three = screening_listboard_page.click(
            description="P3", index=0
        )
        self.assertEqual(add_screening_part_three.status_code, 200)
        return home_page, add_screening_part_three, screening_identifier

    def webtest_for_screening_form_part_three(
        self, home_page, add_screening_part_three, screening_identifier, part_three_data
    ):
        # submit completed form
        for field, _ in add_screening_part_three.form.fields.items():
            try:
                add_screening_part_three.form[field] = part_three_data[field]
            except KeyError:
                print(field)
        page = add_screening_part_three.form.submit()
        soup = BeautifulSoup(page.content, "html.parser")
        errorlist = soup.find_all("ul", "errorlist")
        self.assertEqual([], errorlist)
        # redirects back to listboard
        obj = SubjectScreening.objects.all().last()
        url = reverse(screening_listboard_url, args=(obj.screening_identifier,))
        self.assertRedirects(page, url)
        # shows P1 | P2 | P3 | Consent
        screening_listboard_page = home_page.click(description="Screening", index=1)
        self.assertIn("Consent", screening_listboard_page)
        return screening_listboard_page, screening_identifier

    def get_subject_screening(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        obj = ScreeningPartOne(**part_one_eligible_options)
        obj.save()
        self.screening_identifier = obj.screening_identifier
        obj = ScreeningPartTwo.objects.get(
            screening_identifier=self.screening_identifier
        )
        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        obj = ScreeningPartThree.objects.get(
            screening_identifier=self.screening_identifier
        )
        for k, v in part_three_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        return obj

    @tag("webtest")
    def test_to_subject_dashboard(self):
        add_or_update_django_sites(apps=django_apps, sites=all_sites)
        self.login(superuser=False, groups=[EVERYONE, SCREENING, CLINIC, PII])

        subject_screening = self.get_subject_screening()

        home_page = self.app.get(reverse("home_url"), user=self.user, status=200)
        screening_listboard_page = home_page.click(description="Screening", index=1)

        add_subjectconsent_page = screening_listboard_page.click(
            description="Consent", index=1
        )
        # submit blank form
        response = add_subjectconsent_page.form.submit()
        self.assertIn("Please correct the errors below", response)

        subject_consent = baker.make_recipe(
            "meta_consent.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            dob=(
                get_utcnow() - relativedelta(years=subject_screening.age_in_years)
            ).date(),
            first_name="Melissa",
            last_name="Rodriguez",
            initials="MR",
            consent_datetime=get_utcnow(),
        )

        home_page = self.app.get(reverse("home_url"), user=self.user, status=200)
        screening_listboard_page = home_page.click(description="Screening", index=1)

        self.assertIn("Dashboard", screening_listboard_page)
        self.assertIn(
            f"subjectscreening_change_{subject_screening.screening_identifier}",
            screening_listboard_page,
        )

        home_page = self.app.get(reverse("home_url"), user=self.user, status=200)
        subject_listboard_page = home_page.click(description="Subjects", index=1)

        self.assertIn(subject_consent.subject_identifier, subject_listboard_page)

        href = reverse(
            "meta_dashboard:subject_dashboard_url",
            kwargs={"subject_identifier": subject_consent.subject_identifier},
        )
        subject_dashboard_page = subject_listboard_page.click(href=href)

        self.assertEqual(subject_dashboard_page.status_code, 200)

        # on subject_dashboard
        # assert all appointment are showing
        subject_identifier = subject_consent.subject_identifier
        appointments = Appointment.objects.filter(
            subject_identifier=subject_identifier
        ).order_by("appt_datetime")
        for appointment in appointments:
            self.assertIn(appointment.visit_code, subject_dashboard_page)

        # start appointment 1000
        page = subject_dashboard_page.click(linkid="start_btn_1000")
        page.form["appt_status"] = IN_PROGRESS_APPT
        page.form["appt_reason"] = SCHEDULED_APPT
        subject_dashboard_page = page.form.submit()
        self.assertEqual(subject_dashboard_page.status_code, 302)
        self.assertEqual(
            subject_dashboard_page.url,
            f"/subject/subject_dashboard/{subject_identifier}/",
        )

        subject_dashboard_page = self.app.get(
            subject_dashboard_page.url, user=self.user, status=200
        )

        # start visit 1000
        self.assertIn(" Start ", subject_dashboard_page)
        subject_visit_page = subject_dashboard_page.click(
            linkid=(
                f"start_btn_{appointments[0].visit_code}_"
                f"{appointments[0].visit_code_sequence}"
            )
        )
        subject_visit_page.form["info_source"] = "patient"
        subject_dashboard_page = subject_visit_page.form.submit()

        url = (
            f"/subject/subject_dashboard/{subject_identifier}/"
            f"{str(appointments[0].pk)}/"
        )
        self.assertEqual(subject_dashboard_page.status_code, 302)
        self.assertEqual(subject_dashboard_page.url, url)

        subject_dashboard_page = self.app.get(
            reverse(
                "meta_dashboard:subject_dashboard_url",
                kwargs=dict(
                    subject_identifier=subject_identifier,
                    appointment=str(appointments[0].id),
                ),
            ),
            user=self.user,
            status=200,
        )

        self.assertIn("CRFs", subject_dashboard_page)
        self.assertIn("Requisitions", subject_dashboard_page)

    @tag("webtest")
    def test_follow_urls(self):
        """Follows any url that can be reversed without kwargs."""
        self.login(superuser=False, groups=[EVERYONE, CLINIC, PII])
        for url_name in url_names.registry.values():
            sys.stdout.write(style.MIGRATE_HEADING(f" - '{url_name}' ...\r"))
            try:
                url = reverse(url_name)
            except NoReverseMatch:
                sys.stdout.write(
                    style.ERROR(
                        f" - '{url_name}'. Got `NoReverseMatch` "
                        f"when reversed without kwargs.\n"
                    )
                )
            else:
                try:
                    self.app.get(url, user=self.user, status=200)
                except AppError as e:
                    sys.stdout.write(
                        style.ERROR(f" - '{url_name}'. Got `AppError`: {e}\n")
                    )
                else:
                    sys.stdout.write(style.SUCCESS(f" - '{url_name}'->{url}\n"))
