"""Tests for the writeable (AcroForm) AE TMG Report PDF.

The PDF is emailed to a TMG investigator for completion, so the tests
assert on what a completed file must give back: a stable set of field
names matching the `AeTmg` model fields, and radio values that decode to
the stored value, including `N/A`, which reportlab would otherwise
truncate when writing the PDF name.
"""

from io import BytesIO, StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from clinicedc_constants import GRADE4, NOT_APPLICABLE, OTHER
from clinicedc_constants.choices import YES_NO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, TestCase, override_settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from edc_adverse_event.models import AeClassification
from edc_utils import formatted_date
from model_bakery import baker
from multisite import SiteID
from pypdf import PdfReader, PdfWriter
from pypdf.errors import FileNotDecryptedError

from meta_ae.models import AeInitial
from meta_ae.pdf_forms import (
    INVESTIGATOR_FIELDS,
    AeTmgPdfForm,
    FormCanvas,
    decode_pdf_value,
    encode_choices,
    encode_pdf_value,
    encrypt_pdf,
    generate_password,
    get_ae_classification_choices,
    get_entropy_bits,
    get_revision,
    is_pdf_name_safe,
    render_ae_tmg_pdf_form,
)
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin

LACTIC_ACIDOSIS = "lactic_acidosis"

SIGNATURE_FIELDS = ("signature_name", "signature_date")


class TestPdfValues(SimpleTestCase):
    """`values` does not touch the database."""

    def test_not_applicable_is_not_pdf_name_safe(self):
        self.assertFalse(is_pdf_name_safe(NOT_APPLICABLE))
        self.assertTrue(is_pdf_name_safe(encode_pdf_value(NOT_APPLICABLE)))

    def test_encoded_value_decodes_back_to_stored_value(self):
        choices = ((NOT_APPLICABLE, "Not applicable"), (OTHER, "Other"))
        token = encode_pdf_value(NOT_APPLICABLE)
        self.assertEqual("N_A", token)
        self.assertEqual(NOT_APPLICABLE, decode_pdf_value(token, choices))
        self.assertEqual(NOT_APPLICABLE, decode_pdf_value(f"/{token}", choices))

    def test_blank_or_unknown_token_decodes_to_empty_string(self):
        choices = ((NOT_APPLICABLE, "Not applicable"),)
        for token in ("", "Off", "/Off", "not_a_choice"):
            with self.subTest(token=token):
                self.assertEqual("", decode_pdf_value(token, choices))

    def test_encode_choices_rejects_values_that_collide(self):
        self.assertRaises(ValueError, encode_choices, (("a/b", "one"), ("a b", "two")))

    def test_encode_choices_leaves_safe_values_alone(self):
        choices = (("Yes", "Yes"), ("No", "No"))
        self.assertEqual(choices, encode_choices(choices))


class TestPdfEncryption(SimpleTestCase):
    """`encryption` does not touch the database."""

    @staticmethod
    def make_pdf() -> BytesIO:
        buffer = BytesIO()
        doc = FormCanvas(buffer)
        doc.band("Section")
        doc.textfield("investigator_comments", "Comments:", lines=3)
        doc.save()
        return buffer

    def test_generated_password_is_readable_and_unique(self):
        passwords = {generate_password() for _ in range(50)}
        self.assertEqual(50, len(passwords), "generated passwords repeated")
        for password in passwords:
            with self.subTest(password=password):
                self.assertEqual(5, len(password.split("-")))
                self.assertTrue(password.split("-")[-1].isdigit())

    def test_password_word_count_is_configurable(self):
        self.assertEqual(3, len(generate_password(word_count=2).split("-")))
        self.assertEqual(2, len(generate_password(word_count=2, digits=0).split("-")))

    def test_password_needs_at_least_one_word(self):
        self.assertRaises(ValueError, generate_password, word_count=0)

    def test_entropy_of_the_default_password(self):
        self.assertAlmostEqual(41.3, get_entropy_bits(), places=1)

    def test_encrypt_pdf_refuses_a_blank_password(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.pdf"
            self.assertRaises(ValueError, encrypt_pdf, self.make_pdf(), path, "")
            self.assertFalse(path.exists(), "a plaintext PDF was written")

    def test_encrypted_pdf_does_not_open_without_the_password(self):
        with TemporaryDirectory() as tmp:
            path = encrypt_pdf(self.make_pdf(), Path(tmp) / "out.pdf", "a-password")
            reader = PdfReader(str(path))
            self.assertTrue(reader.is_encrypted)
            with self.assertRaises(FileNotDecryptedError):
                reader.pages[0].extract_text()
            self.assertNotIn(b"investigator_comments", path.read_bytes())

    def test_encrypted_pdf_opens_with_the_password(self):
        with TemporaryDirectory() as tmp:
            path = encrypt_pdf(self.make_pdf(), Path(tmp) / "out.pdf", "a-password")
            reader = PdfReader(str(path))
            self.assertTrue(reader.decrypt("a-password"))
            self.assertEqual(["investigator_comments"], sorted(reader.get_fields() or {}))


class TestFormCanvasRunningText(SimpleTestCase):
    """The header and footer repeat on every page the canvas breaks to."""

    @staticmethod
    def render_multipage(path: Path, header_text: str = "CONFIDENTIAL") -> FormCanvas:
        doc = FormCanvas(str(path))
        doc.header_text = header_text
        doc.footer_text = "main footer"
        doc.footer_subtext = "meta-edc 0.0.0 | Generated 1900-01-01"
        for index in range(10):
            doc.band(f"Section {index}")
            doc.textfield(f"text_{index}", f"Text field {index}:", lines=6)
        doc.save()
        return doc

    def test_header_and_footer_are_drawn_on_each_page(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "multipage.pdf"
            self.render_multipage(path)
            reader = PdfReader(str(path))
            self.assertGreater(len(reader.pages), 1)
            for index, page in enumerate(reader.pages, start=1):
                with self.subTest(page=index):
                    text = page.extract_text()
                    self.assertIn("CONFIDENTIAL", text)
                    self.assertIn("main footer", text)
                    self.assertIn("meta-edc 0.0.0 | Generated 1900-01-01", text)
                    self.assertIn(f"Page {index}", text)

    def test_no_header_is_drawn_when_header_text_is_blank(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "multipage.pdf"
            self.render_multipage(path, header_text="")
            for index, page in enumerate(PdfReader(str(path)).pages, start=1):
                with self.subTest(page=index):
                    text = page.extract_text()
                    self.assertNotIn("CONFIDENTIAL", text)
                    self.assertIn("main footer", text)


@override_settings(SITE_ID=SiteID(10), EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=False)
class TestAeTmgPdfForm(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)

    def get_ae_initial(self, classification_name: str = LACTIC_ACIDOSIS) -> AeInitial:
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        return baker.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=subject_consent.subject_identifier,
            ae_grade=GRADE4,
            ae_classification=AeClassification.objects.get(name=classification_name),
        )

    @staticmethod
    def get_reader(path: Path, password: str = "") -> PdfReader:
        reader = PdfReader(str(path))
        if password:
            reader.decrypt(password)
        return reader

    @classmethod
    def get_fields(cls, path: Path, password: str = "") -> dict:
        return cls.get_reader(path, password).get_fields() or {}

    @classmethod
    def get_text(cls, path: Path, password: str = "") -> str:
        return "\n".join(page.extract_text() for page in cls.get_reader(path, password).pages)

    def test_renders_a_pdf_named_for_the_subject_and_ae_initial(self):
        ae_initial = self.get_ae_initial()
        path = AeTmgPdfForm(ae_initial).render(self.path)
        self.assertTrue(path.exists())
        self.assertGreater(path.stat().st_size, 0)
        self.assertIn(ae_initial.subject_identifier, path.name)
        self.assertIn(ae_initial.action_identifier[-9:], path.name)

    def test_renders_to_an_explicit_filename(self):
        path = render_ae_tmg_pdf_form(self.get_ae_initial(), self.path / "ae_tmg.pdf")
        self.assertEqual("ae_tmg.pdf", path.name)
        self.assertTrue(path.exists())

    def test_writeable_fields_are_the_investigator_fields_and_signature(self):
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path)
        self.assertEqual(
            sorted((*INVESTIGATOR_FIELDS, *SIGNATURE_FIELDS)),
            sorted(self.get_fields(path)),
        )

    def test_writeable_fields_start_blank(self):
        fields = self.get_fields(AeTmgPdfForm(self.get_ae_initial()).render(self.path))
        for name in (*INVESTIGATOR_FIELDS, *SIGNATURE_FIELDS):
            with self.subTest(name=name):
                self.assertIn(fields[name].get("/V") or "", ("", "/Off", None))

    def test_original_report_is_drawn_as_text_not_as_a_field(self):
        ae_initial = self.get_ae_initial()
        path = AeTmgPdfForm(ae_initial).render(self.path)
        text = self.get_text(path)
        for expected in (
            ae_initial.subject_identifier,
            ae_initial.action_identifier,
            ae_initial.ae_classification.display_name,
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        self.assertNotIn("subject_identifier", self.get_fields(path))
        self.assertNotIn("ae_description", self.get_fields(path))

    def test_ae_classification_other_is_appended_to_the_original_classification(self):
        ae_initial = self.get_ae_initial(classification_name=OTHER)
        ae_initial.ae_classification_other = "some other classification"
        ae_initial.save()
        self.assertIn(
            "some other classification", AeTmgPdfForm(ae_initial).ae_classification_display
        )

    def test_confidential_header_is_on_every_page(self):
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path)
        for index, page in enumerate(PdfReader(str(path)).pages, start=1):
            with self.subTest(page=index):
                self.assertIn("CONFIDENTIAL", page.extract_text())

    def test_footer_carries_the_revision_and_generated_date(self):
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path)
        expected = (
            f"meta-edc {get_revision()} | Generated {formatted_date(timezone.localdate())}"
        )
        for index, page in enumerate(PdfReader(str(path)).pages, start=1):
            with self.subTest(page=index):
                self.assertIn(expected, page.extract_text())

    def test_revision_is_the_installed_pyproject_version(self):
        """The distribution is installed, so the version must not be blank."""
        self.assertTrue(get_revision())
        self.assertEqual(get_revision(), AeTmgPdfForm(self.get_ae_initial()).revision)

    def test_labels_come_from_the_model_verbose_name(self):
        for field_name in ("investigator_comments", "report_status"):
            with self.subTest(field_name=field_name):
                verbose_name = str(AeTmgPdfForm.get_field(field_name).verbose_name).strip()
                self.assertIn(
                    verbose_name.rstrip(":."),
                    self.get_text(AeTmgPdfForm(self.get_ae_initial()).render(self.path)),
                )

    def test_renders_a_lazy_verbose_name(self):
        """reportlab cannot render a lazy translation object, so it is resolved."""
        field = AeTmgPdfForm.get_field("investigator_comments")
        original = field.verbose_name
        field.verbose_name = _("A lazy verbose name")
        self.addCleanup(setattr, field, "verbose_name", original)
        self.assertNotIsInstance(field.verbose_name, str)
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path)
        self.assertIn("A lazy verbose name", self.get_text(path))

    def test_renders_a_lazy_help_text(self):
        field = AeTmgPdfForm.get_field("investigator_ae_classification")
        original = field.help_text
        field.help_text = _("a lazy help text")
        self.addCleanup(setattr, field, "help_text", original)
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path)
        self.assertIn("a lazy help text", self.get_text(path))

    def test_renders_a_lazy_header_and_footer(self):
        form = AeTmgPdfForm(self.get_ae_initial())
        form.header_text = _("CONFIDENTIAL")
        self.assertNotIsInstance(form.header_text, str)
        self.assertIn("CONFIDENTIAL", self.get_text(form.render(self.path)))

    def test_lazy_choice_labels_are_rendered(self):
        """`YES_NO` labels are `gettext_lazy` objects."""
        text = self.get_text(AeTmgPdfForm(self.get_ae_initial()).render(self.path))
        for _value, display in YES_NO:
            with self.subTest(display=display):
                self.assertIn(str(display), text)

    def test_renders_unencrypted_when_no_password_is_given(self):
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path)
        self.assertFalse(PdfReader(str(path)).is_encrypted)

    def test_renders_encrypted_when_a_password_is_given(self):
        password = generate_password()
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path, password=password)
        reader = PdfReader(str(path))
        self.assertTrue(reader.is_encrypted)
        with self.assertRaises(FileNotDecryptedError):
            reader.pages[0].extract_text()

    def test_encrypted_form_keeps_every_writeable_field(self):
        password = generate_password()
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path, password=password)
        self.assertEqual(
            sorted((*INVESTIGATOR_FIELDS, *SIGNATURE_FIELDS)),
            sorted(self.get_fields(path, password)),
        )
        self.assertIn("CONFIDENTIAL", self.get_text(path, password))

    def test_encrypted_form_is_still_fillable(self):
        password = generate_password()
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path, password=password)
        filled = self.path / "filled.pdf"
        writer = PdfWriter(clone_from=self.get_reader(path, password))
        writer.update_page_form_field_values(
            writer.pages[0],
            {"investigator_comments": "typed after decryption"},
            auto_regenerate=False,
        )
        writer.write(str(filled))
        self.assertEqual(
            "typed after decryption",
            self.get_fields(filled)["investigator_comments"].get("/V"),
        )

    def test_classification_radio_offers_every_ae_classification(self):
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path)
        states = self.get_radio_states(path, "investigator_ae_classification")
        choices = get_ae_classification_choices()
        self.assertEqual(
            sorted(value for value, _ in choices),
            sorted(decode_pdf_value(state, choices) for state in states),
        )

    def test_not_applicable_classification_survives_the_round_trip(self):
        """`N/A` is written as the PDF name `/N_A`, not truncated to `/N`."""
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path)
        filled = self.path / "filled.pdf"
        writer = PdfWriter(clone_from=str(path))
        writer.update_page_form_field_values(
            writer.pages[0],
            {"investigator_ae_classification": f"/{encode_pdf_value(NOT_APPLICABLE)}"},
            auto_regenerate=False,
        )
        writer.write(str(filled))
        value = self.get_fields(filled)["investigator_ae_classification"].get("/V")
        self.assertEqual(
            NOT_APPLICABLE, decode_pdf_value(str(value), get_ae_classification_choices())
        )

    def test_typed_text_reads_back(self):
        path = AeTmgPdfForm(self.get_ae_initial()).render(self.path)
        filled = self.path / "filled.pdf"
        writer = PdfWriter(clone_from=str(path))
        writer.update_page_form_field_values(
            writer.pages[0],
            {"investigator_comments": "this investigator disagrees"},
            auto_regenerate=False,
        )
        writer.write(str(filled))
        self.assertEqual(
            "this investigator disagrees",
            self.get_fields(filled)["investigator_comments"].get("/V"),
        )

    @staticmethod
    def get_radio_states(path: Path, name: str) -> list[str]:
        """Returns the export values offered by radio group `name`."""
        states = []
        for page in PdfReader(str(path)).pages:
            for annot in page.get("/Annots") or []:
                obj = annot.get_object()
                parent = obj.get("/Parent")
                field_name = obj.get("/T") or (
                    parent.get_object().get("/T") if parent else None
                )
                if str(field_name) != name:
                    continue
                appearances = obj.get("/AP").get_object().get("/N").get_object()
                states.extend(str(k) for k in appearances if str(k) != "/Off")
        return states


@override_settings(SITE_ID=SiteID(10), EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=False)
class TestGenerateAeTmgPdfFormCommand(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)

    def get_ae_initial(self) -> AeInitial:
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        return baker.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=subject_consent.subject_identifier,
            ae_grade=GRADE4,
            ae_classification=AeClassification.objects.get(name=LACTIC_ACIDOSIS),
        )

    def generate(self, **kwargs) -> str:
        out = StringIO()
        call_command("generate_ae_tmg_pdf_form", stdout=out, path=str(self.path), **kwargs)
        return out.getvalue()

    def test_generates_one_pdf_for_an_action_identifier(self):
        ae_initial = self.get_ae_initial()
        self.generate(action_identifier=ae_initial.action_identifier)
        self.assertEqual(1, len(list(self.path.glob("*.pdf"))))

    def test_generates_one_pdf_per_ae_initial_for_a_subject(self):
        ae_initial = self.get_ae_initial()
        baker.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=ae_initial.subject_identifier,
            ae_grade=GRADE4,
            ae_classification=AeClassification.objects.get(name=LACTIC_ACIDOSIS),
        )
        self.generate(subject_identifier=ae_initial.subject_identifier)
        self.assertEqual(2, len(list(self.path.glob("*.pdf"))))

    def test_prints_a_password_that_opens_the_pdf(self):
        ae_initial = self.get_ae_initial()
        out = self.generate(action_identifier=ae_initial.action_identifier)
        (password,) = [
            line.split("Password: ", 1)[1].strip()
            for line in out.splitlines()
            if line.startswith("Password: ")
        ]
        (path,) = list(self.path.glob("*.pdf"))
        reader = PdfReader(str(path))
        self.assertTrue(reader.is_encrypted)
        self.assertTrue(reader.decrypt(password))
        self.assertEqual(
            sorted((*INVESTIGATOR_FIELDS, *SIGNATURE_FIELDS)),
            sorted(reader.get_fields() or {}),
        )

    def test_prints_one_password_per_form(self):
        ae_initial = self.get_ae_initial()
        baker.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=ae_initial.subject_identifier,
            ae_grade=GRADE4,
            ae_classification=AeClassification.objects.get(name=LACTIC_ACIDOSIS),
        )
        out = self.generate(subject_identifier=ae_initial.subject_identifier)
        passwords = [line for line in out.splitlines() if line.startswith("Password: ")]
        self.assertEqual(2, len(passwords))
        self.assertEqual(2, len(set(passwords)), "the same password was reused")

    def test_raises_without_an_identifier(self):
        self.assertRaises(CommandError, self.generate)

    def test_raises_with_both_identifiers(self):
        ae_initial = self.get_ae_initial()
        self.assertRaises(
            CommandError,
            self.generate,
            action_identifier=ae_initial.action_identifier,
            subject_identifier=ae_initial.subject_identifier,
        )

    def test_raises_when_nothing_matches(self):
        self.assertRaises(CommandError, self.generate, action_identifier="does-not-exist")
