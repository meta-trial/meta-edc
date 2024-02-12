# Generated by Django 5.0.1 on 2024-02-12 14:01

import _socket
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import edc_action_item.managers
import edc_model.models.fields.date_estimated
import edc_model.validators.date
import edc_protocol.validators
import edc_sites.managers
import edc_utils.date
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_action_item", "0036_alter_actionitem_priority_alter_actionitem_site_and_more"),
        ("meta_ae", "0021_alter_aefollowup_site_alter_aeinitial_site_and_more"),
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalHospitalization",
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
                ("subject_identifier", models.CharField(max_length=50)),
                (
                    "action_identifier",
                    models.CharField(blank=True, db_index=True, max_length=50, null=True),
                ),
                (
                    "parent_action_identifier",
                    models.CharField(
                        blank=True,
                        help_text="action identifier that links to parent reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "related_action_identifier",
                    models.CharField(
                        blank=True,
                        help_text="action identifier that links to related reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                ("action_item_reason", models.TextField(editable=False, null=True)),
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow,
                        validators=[
                            edc_protocol.validators.datetime_not_before_study_start,
                            edc_model.validators.date.datetime_not_future,
                        ],
                        verbose_name="Report Date",
                    ),
                ),
                (
                    "have_details",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=15,
                        verbose_name="Do you have details of the hospitalization?",
                    ),
                ),
                (
                    "admitted_date",
                    models.DateField(
                        validators=[
                            edc_model.validators.date.date_not_future,
                            edc_protocol.validators.date_not_before_study_start,
                        ],
                        verbose_name="When was the patient admitted?",
                    ),
                ),
                (
                    "admitted_date_estimated",
                    edc_model.models.fields.date_estimated.IsDateEstimatedField(
                        choices=[
                            ("-", "No"),
                            ("D", "Yes, estimated the Day"),
                            ("MD", "Yes, estimated Month and Day"),
                            ("YMD", "Yes, estimated Year, Month and Day"),
                        ],
                        help_text="If the exact date is not known, please indicate which part of the date is estimated.",
                        max_length=25,
                        verbose_name="Is this date estimated?",
                    ),
                ),
                (
                    "discharged",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No"), ("unknown", "Unknown")],
                        max_length=15,
                        verbose_name="Has the patient been discharged?",
                    ),
                ),
                (
                    "discharged_date",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[
                            edc_model.validators.date.date_not_future,
                            edc_protocol.validators.date_not_before_study_start,
                        ],
                        verbose_name="If YES, give date discharged",
                    ),
                ),
                (
                    "discharged_date_estimated",
                    edc_model.models.fields.date_estimated.IsDateEstimatedFieldNa(
                        choices=[
                            ("N/A", "Not applicable"),
                            ("not_estimated", "No"),
                            ("D", "Yes, estimated the Day"),
                            ("MD", "Yes, estimated Month and Day"),
                            ("YMD", "Yes, estimated Year, Month and Day"),
                        ],
                        default="N/A",
                        help_text="If the exact date is not known, please indicate which part of the date is estimated.",
                        max_length=25,
                        verbose_name="If YES, is this date estimated?",
                    ),
                ),
                (
                    "narrative",
                    models.TextField(
                        blank=True, max_length=500, null=True, verbose_name="Narrative"
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
                    "action_item",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_action_item.actionitem",
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
                    "parent_action_item",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_action_item.actionitem",
                    ),
                ),
                (
                    "related_action_item",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_action_item.actionitem",
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
            ],
            options={
                "verbose_name": "historical Hospitalization",
                "verbose_name_plural": "historical Hospitalization",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="Hospitalization",
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
                ("subject_identifier", models.CharField(max_length=50)),
                (
                    "action_identifier",
                    models.CharField(blank=True, max_length=50, null=True, unique=True),
                ),
                (
                    "parent_action_identifier",
                    models.CharField(
                        blank=True,
                        help_text="action identifier that links to parent reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "related_action_identifier",
                    models.CharField(
                        blank=True,
                        help_text="action identifier that links to related reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                ("action_item_reason", models.TextField(editable=False, null=True)),
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow,
                        validators=[
                            edc_protocol.validators.datetime_not_before_study_start,
                            edc_model.validators.date.datetime_not_future,
                        ],
                        verbose_name="Report Date",
                    ),
                ),
                (
                    "have_details",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=15,
                        verbose_name="Do you have details of the hospitalization?",
                    ),
                ),
                (
                    "admitted_date",
                    models.DateField(
                        validators=[
                            edc_model.validators.date.date_not_future,
                            edc_protocol.validators.date_not_before_study_start,
                        ],
                        verbose_name="When was the patient admitted?",
                    ),
                ),
                (
                    "admitted_date_estimated",
                    edc_model.models.fields.date_estimated.IsDateEstimatedField(
                        choices=[
                            ("-", "No"),
                            ("D", "Yes, estimated the Day"),
                            ("MD", "Yes, estimated Month and Day"),
                            ("YMD", "Yes, estimated Year, Month and Day"),
                        ],
                        help_text="If the exact date is not known, please indicate which part of the date is estimated.",
                        max_length=25,
                        verbose_name="Is this date estimated?",
                    ),
                ),
                (
                    "discharged",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No"), ("unknown", "Unknown")],
                        max_length=15,
                        verbose_name="Has the patient been discharged?",
                    ),
                ),
                (
                    "discharged_date",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[
                            edc_model.validators.date.date_not_future,
                            edc_protocol.validators.date_not_before_study_start,
                        ],
                        verbose_name="If YES, give date discharged",
                    ),
                ),
                (
                    "discharged_date_estimated",
                    edc_model.models.fields.date_estimated.IsDateEstimatedFieldNa(
                        choices=[
                            ("N/A", "Not applicable"),
                            ("not_estimated", "No"),
                            ("D", "Yes, estimated the Day"),
                            ("MD", "Yes, estimated Month and Day"),
                            ("YMD", "Yes, estimated Year, Month and Day"),
                        ],
                        default="N/A",
                        help_text="If the exact date is not known, please indicate which part of the date is estimated.",
                        max_length=25,
                        verbose_name="If YES, is this date estimated?",
                    ),
                ),
                (
                    "narrative",
                    models.TextField(
                        blank=True, max_length=500, null=True, verbose_name="Narrative"
                    ),
                ),
                (
                    "action_item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="edc_action_item.actionitem",
                    ),
                ),
                (
                    "parent_action_item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="edc_action_item.actionitem",
                    ),
                ),
                (
                    "related_action_item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="edc_action_item.actionitem",
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
            ],
            options={
                "verbose_name": "Hospitalization",
                "verbose_name_plural": "Hospitalization",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "default_manager_name": "objects",
                "indexes": [
                    models.Index(
                        fields=["subject_identifier"], name="meta_ae_hos_subject_605b97_idx"
                    ),
                    models.Index(
                        fields=["modified", "created"], name="meta_ae_hos_modifie_8fcf1c_idx"
                    ),
                    models.Index(
                        fields=["user_modified", "user_created"],
                        name="meta_ae_hos_user_mo_99daf8_idx",
                    ),
                    models.Index(
                        fields=["subject_identifier", "site"],
                        name="meta_ae_hos_subject_9cbfad_idx",
                    ),
                ],
            },
            managers=[
                ("on_site", edc_sites.managers.CurrentSiteManager()),
                ("objects", edc_action_item.managers.ActionIdentifierModelManager()),
            ],
        ),
    ]
