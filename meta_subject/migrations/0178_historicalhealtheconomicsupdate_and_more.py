# Generated by Django 4.2.10 on 2024-02-22 23:41

import _socket
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import edc_crf.model_mixins.crf_status_model_mixin
import edc_model.validators.date
import edc_model_fields.fields.other_charfield
import edc_protocol.validators
import edc_utils.date
import edc_visit_tracking.managers
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("meta_subject", "0177_alter_bloodresultslft_alp_value_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalHealthEconomicsUpdate",
            fields=[
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "user_created",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                        verbose_name="Hostname created",
                    ),
                ),
                (
                    "hostname_modified",
                    django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                        verbose_name="Hostname modified",
                    ),
                ),
                (
                    "device_created",
                    models.CharField(blank=True, max_length=10, verbose_name="Device created"),
                ),
                (
                    "device_modified",
                    models.CharField(
                        blank=True, max_length=10, verbose_name="Device modified"
                    ),
                ),
                (
                    "locale_created",
                    models.CharField(
                        blank=True,
                        help_text="Auto-updated by Modeladmin",
                        max_length=10,
                        null=True,
                        verbose_name="Locale created",
                    ),
                ),
                (
                    "locale_modified",
                    models.CharField(
                        blank=True,
                        help_text="Auto-updated by Modeladmin",
                        max_length=10,
                        null=True,
                        verbose_name="Locale modified",
                    ),
                ),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                    ),
                ),
                ("consent_model", models.CharField(editable=False, max_length=50, null=True)),
                (
                    "consent_version",
                    models.CharField(editable=False, max_length=10, null=True),
                ),
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow,
                        help_text="If reporting today, use today's date/time, otherwise use the date/time this information was reported.",
                        validators=[
                            edc_protocol.validators.datetime_not_before_study_start,
                            edc_model.validators.date.datetime_not_future,
                        ],
                        verbose_name="Report Date",
                    ),
                ),
                (
                    "crf_status",
                    models.CharField(
                        choices=[
                            ("INCOMPLETE", "Incomplete (some data pending)"),
                            ("COMPLETE", "Complete"),
                        ],
                        default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                        help_text="If some data is still pending, flag this CRF as incomplete",
                        max_length=25,
                        verbose_name="CRF status",
                    ),
                ),
                (
                    "crf_status_comments",
                    models.TextField(
                        blank=True,
                        help_text="for example, why some data is still pending",
                        null=True,
                        verbose_name="Any comments related to status of this CRF",
                    ),
                ),
                (
                    "hh_count",
                    models.IntegerField(
                        help_text="Persons",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(25),
                        ],
                        verbose_name="What is the total number of people who live in your household?",
                    ),
                ),
                (
                    "hh_minors_count",
                    models.IntegerField(
                        help_text="Persons",
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(25),
                        ],
                        verbose_name="What is the total number of people 14 years or under who live in your household?",
                    ),
                ),
                (
                    "avg_income",
                    models.CharField(
                        choices=[
                            ("Yes", "Yes"),
                            ("No", "No"),
                            ("dont_know", "Don't know"),
                            ("DWTA", "Don't want to answer"),
                        ],
                        help_text=None,
                        max_length=15,
                        verbose_name="Thinking over the last 12 months, can you tell me what the average earnings of the household have been?",
                    ),
                ),
                (
                    "avg_income_value_known",
                    models.CharField(
                        choices=[
                            ("weekly", "as weekly income"),
                            ("monthly", "as monthly income"),
                            ("yearly", "as yearly income"),
                            ("dont_know", "Don't know"),
                            ("DWTA", "Don't want to answer"),
                            ("N/A", "Not applicable"),
                        ],
                        default="N/A",
                        max_length=15,
                        verbose_name="Over which <u>time period</u> are you able to estimate?",
                    ),
                ),
                (
                    "avg_income_value",
                    models.IntegerField(
                        blank=True,
                        help_text="Use cash equivalent in local currency",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(999999999),
                        ],
                        verbose_name="Estimated <u>total amount of income</u> from this source over the time period from above",
                    ),
                ),
                (
                    "hoh",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        help_text="By head of the household we mean the main decision maker in the household. The head can be either male or female. If two people are equal decision-makers, take the older person.",
                        max_length=15,
                        verbose_name="Are you the household head?",
                    ),
                ),
                (
                    "relationship_to_hoh",
                    models.CharField(
                        choices=[
                            ("WIFE_HUSBAND", "Wife/Husband"),
                            ("SON_DAUGHTER", "Son/Daughter"),
                            ("SON_DAUGHTERINLAW", "Son/Daughter-in-law"),
                            ("GRANDCHILD", "Grandchild"),
                            ("PARENT", "Parent"),
                            ("PARENTINLAW", "Parent-in-law"),
                            ("BROTHER_SISTER", "Brother/Sister"),
                            ("OTHER", "Other, specify ..."),
                            ("dont_know", "Don't know"),
                            ("N/A", "Not applicable"),
                        ],
                        default="N/A",
                        help_text="Not applicable if patient is head of household",
                        max_length=25,
                        verbose_name="If No, what is your relationship to the household head?",
                    ),
                ),
                (
                    "relationship_to_hoh_other",
                    edc_model_fields.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If OTHER relationship, specify ...",
                    ),
                ),
                (
                    "rooms",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(30),
                        ],
                        verbose_name="How many rooms does your dwelling have in total, without counting the bathrooms/ toilets or hallways/passageways?",
                    ),
                ),
                (
                    "bedrooms",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(30),
                        ],
                        verbose_name="How many rooms are used for sleeping in your dwelling?",
                    ),
                ),
                (
                    "beds",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(30),
                        ],
                        verbose_name="How many beds does your dwelling have in total?",
                    ),
                ),
                (
                    "external_dependents",
                    models.IntegerField(
                        help_text="Insert '0' if no dependents other than the members in the household roster",
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(15),
                        ],
                        verbose_name="Outside of this household, how many other people depend on this household’s income?",
                    ),
                ),
                (
                    "financial_status",
                    models.CharField(
                        choices=[
                            ("1", "Very good"),
                            ("2", "Good"),
                            ("3", "Moderate"),
                            ("4", "Bad"),
                            ("5", "Very bad"),
                            ("DWTA", "Don't want to answer"),
                        ],
                        max_length=25,
                        verbose_name="Would you say your household's financial situation is?",
                    ),
                ),
                (
                    "history_id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="sites.site",
                    ),
                ),
                (
                    "subject_visit",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="meta_subject.subjectvisit",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Health Economics: Baseline",
                "verbose_name_plural": "historical Health Economics: Baseline",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HealthEconomicsUpdate",
            fields=[
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "user_created",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                        verbose_name="Hostname created",
                    ),
                ),
                (
                    "hostname_modified",
                    django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                        verbose_name="Hostname modified",
                    ),
                ),
                (
                    "device_created",
                    models.CharField(blank=True, max_length=10, verbose_name="Device created"),
                ),
                (
                    "device_modified",
                    models.CharField(
                        blank=True, max_length=10, verbose_name="Device modified"
                    ),
                ),
                (
                    "locale_created",
                    models.CharField(
                        blank=True,
                        help_text="Auto-updated by Modeladmin",
                        max_length=10,
                        null=True,
                        verbose_name="Locale created",
                    ),
                ),
                (
                    "locale_modified",
                    models.CharField(
                        blank=True,
                        help_text="Auto-updated by Modeladmin",
                        max_length=10,
                        null=True,
                        verbose_name="Locale modified",
                    ),
                ),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("consent_model", models.CharField(editable=False, max_length=50, null=True)),
                (
                    "consent_version",
                    models.CharField(editable=False, max_length=10, null=True),
                ),
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow,
                        help_text="If reporting today, use today's date/time, otherwise use the date/time this information was reported.",
                        validators=[
                            edc_protocol.validators.datetime_not_before_study_start,
                            edc_model.validators.date.datetime_not_future,
                        ],
                        verbose_name="Report Date",
                    ),
                ),
                (
                    "crf_status",
                    models.CharField(
                        choices=[
                            ("INCOMPLETE", "Incomplete (some data pending)"),
                            ("COMPLETE", "Complete"),
                        ],
                        default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                        help_text="If some data is still pending, flag this CRF as incomplete",
                        max_length=25,
                        verbose_name="CRF status",
                    ),
                ),
                (
                    "crf_status_comments",
                    models.TextField(
                        blank=True,
                        help_text="for example, why some data is still pending",
                        null=True,
                        verbose_name="Any comments related to status of this CRF",
                    ),
                ),
                (
                    "hh_count",
                    models.IntegerField(
                        help_text="Persons",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(25),
                        ],
                        verbose_name="What is the total number of people who live in your household?",
                    ),
                ),
                (
                    "hh_minors_count",
                    models.IntegerField(
                        help_text="Persons",
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(25),
                        ],
                        verbose_name="What is the total number of people 14 years or under who live in your household?",
                    ),
                ),
                (
                    "avg_income",
                    models.CharField(
                        choices=[
                            ("Yes", "Yes"),
                            ("No", "No"),
                            ("dont_know", "Don't know"),
                            ("DWTA", "Don't want to answer"),
                        ],
                        help_text=None,
                        max_length=15,
                        verbose_name="Thinking over the last 12 months, can you tell me what the average earnings of the household have been?",
                    ),
                ),
                (
                    "avg_income_value_known",
                    models.CharField(
                        choices=[
                            ("weekly", "as weekly income"),
                            ("monthly", "as monthly income"),
                            ("yearly", "as yearly income"),
                            ("dont_know", "Don't know"),
                            ("DWTA", "Don't want to answer"),
                            ("N/A", "Not applicable"),
                        ],
                        default="N/A",
                        max_length=15,
                        verbose_name="Over which <u>time period</u> are you able to estimate?",
                    ),
                ),
                (
                    "avg_income_value",
                    models.IntegerField(
                        blank=True,
                        help_text="Use cash equivalent in local currency",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(999999999),
                        ],
                        verbose_name="Estimated <u>total amount of income</u> from this source over the time period from above",
                    ),
                ),
                (
                    "hoh",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        help_text="By head of the household we mean the main decision maker in the household. The head can be either male or female. If two people are equal decision-makers, take the older person.",
                        max_length=15,
                        verbose_name="Are you the household head?",
                    ),
                ),
                (
                    "relationship_to_hoh",
                    models.CharField(
                        choices=[
                            ("WIFE_HUSBAND", "Wife/Husband"),
                            ("SON_DAUGHTER", "Son/Daughter"),
                            ("SON_DAUGHTERINLAW", "Son/Daughter-in-law"),
                            ("GRANDCHILD", "Grandchild"),
                            ("PARENT", "Parent"),
                            ("PARENTINLAW", "Parent-in-law"),
                            ("BROTHER_SISTER", "Brother/Sister"),
                            ("OTHER", "Other, specify ..."),
                            ("dont_know", "Don't know"),
                            ("N/A", "Not applicable"),
                        ],
                        default="N/A",
                        help_text="Not applicable if patient is head of household",
                        max_length=25,
                        verbose_name="If No, what is your relationship to the household head?",
                    ),
                ),
                (
                    "relationship_to_hoh_other",
                    edc_model_fields.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If OTHER relationship, specify ...",
                    ),
                ),
                (
                    "rooms",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(30),
                        ],
                        verbose_name="How many rooms does your dwelling have in total, without counting the bathrooms/ toilets or hallways/passageways?",
                    ),
                ),
                (
                    "bedrooms",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(30),
                        ],
                        verbose_name="How many rooms are used for sleeping in your dwelling?",
                    ),
                ),
                (
                    "beds",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(30),
                        ],
                        verbose_name="How many beds does your dwelling have in total?",
                    ),
                ),
                (
                    "external_dependents",
                    models.IntegerField(
                        help_text="Insert '0' if no dependents other than the members in the household roster",
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(15),
                        ],
                        verbose_name="Outside of this household, how many other people depend on this household’s income?",
                    ),
                ),
                (
                    "financial_status",
                    models.CharField(
                        choices=[
                            ("1", "Very good"),
                            ("2", "Good"),
                            ("3", "Moderate"),
                            ("4", "Bad"),
                            ("5", "Very bad"),
                            ("DWTA", "Don't want to answer"),
                        ],
                        max_length=25,
                        verbose_name="Would you say your household's financial situation is?",
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="sites.site",
                    ),
                ),
                (
                    "subject_visit",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="meta_subject.subjectvisit",
                    ),
                ),
            ],
            options={
                "verbose_name": "Health Economics: Baseline",
                "verbose_name_plural": "Health Economics: Baseline",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "default_manager_name": "objects",
                "indexes": [
                    models.Index(
                        fields=["subject_visit", "site"], name="meta_subjec_subject_40c4fc_idx"
                    ),
                    models.Index(
                        fields=["subject_visit", "report_datetime"],
                        name="meta_subjec_subject_948b63_idx",
                    ),
                ],
            },
            managers=[
                ("objects", edc_visit_tracking.managers.CrfModelManager()),
                ("on_site", edc_visit_tracking.managers.CrfCurrentSiteManager()),
            ],
        ),
    ]
