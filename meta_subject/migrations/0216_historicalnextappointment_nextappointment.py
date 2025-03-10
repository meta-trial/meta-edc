# Generated by Django 6.0 on 2025-01-28 13:32

import _socket
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import edc_crf.model_mixins.crf_status_model_mixin
import edc_model.validators.date
import edc_protocol.validators
import edc_utils.date
import edc_visit_tracking.managers
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_appointment", "0048_alter_appointment_site_and_more"),
        ("edc_facility", "0014_healthfacility_title_historicalhealthfacility_title"),
        ("edc_visit_schedule", "0017_alter_onschedule_managers"),
        ("meta_subject", "0215_alter_historicalstudymedication_stock_codes_and_more"),
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalNextAppointment",
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
                        blank=True,
                        default=django_audit_fields.models.audit_model_mixin.utcnow,
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True,
                        default=django_audit_fields.models.audit_model_mixin.utcnow,
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
                (
                    "consent_model",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "consent_version",
                    models.CharField(blank=True, max_length=10, null=True),
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
                    "appt_date",
                    models.DateField(
                        help_text="Should fall on an valid clinic day for this facility",
                        null=True,
                        verbose_name="Next scheduled routine/facility appointment",
                    ),
                ),
                (
                    "appt_datetime",
                    models.DateField(
                        help_text="Should fall on an valid clinic day for this facility",
                        null=True,
                        verbose_name="Next scheduled routine/facility appointment date and time",
                    ),
                ),
                (
                    "allow_create_interim",
                    models.BooleanField(
                        default=False,
                        help_text="Override date check to allow the EDC to create an interim appointment if the date is within window period of the current appointment.",
                        verbose_name="Override date check?",
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
                    "history_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
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
                    "health_facility",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_facility.healthfacility",
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
                    "info_source",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        max_length=15,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_appointment.infosources",
                        verbose_name="What is the source of this appointment date",
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
                (
                    "visitschedule",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        help_text="Click SAVE to let the EDC suggest. Once selected, interim appointments will be flagged as not required/missed.",
                        max_length=15,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_visit_schedule.visitschedule",
                        verbose_name="Which study visit code is closest to this appointment date",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Next Appointment",
                "verbose_name_plural": "historical Next Appointments",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="NextAppointment",
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
                        blank=True,
                        default=django_audit_fields.models.audit_model_mixin.utcnow,
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True,
                        default=django_audit_fields.models.audit_model_mixin.utcnow,
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
                (
                    "consent_model",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "consent_version",
                    models.CharField(blank=True, max_length=10, null=True),
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
                    "appt_date",
                    models.DateField(
                        help_text="Should fall on an valid clinic day for this facility",
                        null=True,
                        verbose_name="Next scheduled routine/facility appointment",
                    ),
                ),
                (
                    "appt_datetime",
                    models.DateField(
                        help_text="Should fall on an valid clinic day for this facility",
                        null=True,
                        verbose_name="Next scheduled routine/facility appointment date and time",
                    ),
                ),
                (
                    "allow_create_interim",
                    models.BooleanField(
                        default=False,
                        help_text="Override date check to allow the EDC to create an interim appointment if the date is within window period of the current appointment.",
                        verbose_name="Override date check?",
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
                    "health_facility",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="edc_facility.healthfacility",
                    ),
                ),
                (
                    "info_source",
                    models.ForeignKey(
                        max_length=15,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="edc_appointment.infosources",
                        verbose_name="What is the source of this appointment date",
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
                (
                    "visitschedule",
                    models.ForeignKey(
                        help_text="Click SAVE to let the EDC suggest. Once selected, interim appointments will be flagged as not required/missed.",
                        max_length=15,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="edc_visit_schedule.visitschedule",
                        verbose_name="Which study visit code is closest to this appointment date",
                    ),
                ),
            ],
            options={
                "verbose_name": "Next Appointment",
                "verbose_name_plural": "Next Appointments",
                "abstract": False,
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "default_manager_name": "objects",
                "indexes": [
                    models.Index(
                        fields=["subject_visit", "site"],
                        name="meta_subjec_subject_0d7238_idx",
                    ),
                    models.Index(
                        fields=["subject_visit", "report_datetime"],
                        name="meta_subjec_subject_208c45_idx",
                    ),
                    models.Index(
                        fields=["modified", "created"],
                        name="meta_subjec_modifie_0f17e9_idx",
                    ),
                    models.Index(
                        fields=["user_modified", "user_created"],
                        name="meta_subjec_user_mo_c4e256_idx",
                    ),
                ],
            },
            managers=[
                ("objects", edc_visit_tracking.managers.CrfModelManager()),
                ("on_site", edc_visit_tracking.managers.CrfCurrentSiteManager()),
            ],
        ),
    ]
