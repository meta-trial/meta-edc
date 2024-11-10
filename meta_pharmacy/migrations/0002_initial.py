# Generated by Django 5.1 on 2024-09-09 20:35

import uuid

import _socket
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import edc_pharmacy.models.prescription.rx
import edc_sites.managers
import edc_utils.date
import simple_history.models
from django.conf import settings
from django.db import migrations, models

import meta_pharmacy.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("edc_action_item", "0037_remove_actionitem_reference_model_and_more"),
        ("edc_pharmacy", "0023_remove_rx_edc_pharmac_modifie_986021_idx_and_more"),
        ("meta_pharmacy", "0001_initial"),
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Rx",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("edc_pharmacy.rx",),
            managers=[
                ("objects", edc_pharmacy.models.prescription.rx.Manager()),
                ("on_site", edc_sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalRx",
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
                    "slug",
                    models.CharField(
                        db_index=True,
                        default="",
                        editable=False,
                        help_text="a field used for quick search",
                        max_length=250,
                        null=True,
                    ),
                ),
                (
                    "rx_identifier",
                    models.CharField(db_index=True, default=uuid.uuid4, max_length=36),
                ),
                ("rx_name", models.CharField(default="study prescription", max_length=36)),
                ("report_datetime", models.DateTimeField(default=edc_utils.date.get_utcnow)),
                (
                    "rx_date",
                    models.DateField(
                        default=edc_utils.date.get_utcnow, verbose_name="Date RX written"
                    ),
                ),
                (
                    "rx_expiration_date",
                    models.DateField(
                        blank=True,
                        help_text="Leave blank. Will be filled when end of study report is submitted",
                        null=True,
                        verbose_name="Date RX expires",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("New", "New"),
                            ("partial", "Partially filled"),
                            ("filled", "Filled"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="New",
                        max_length=25,
                    ),
                ),
                (
                    "refill",
                    models.IntegerField(
                        blank=True,
                        help_text="Number of times this prescription may be refilled",
                        null=True,
                    ),
                ),
                ("rando_sid", models.CharField(blank=True, max_length=25, null=True)),
                ("randomizer_name", models.CharField(blank=True, max_length=25, null=True)),
                (
                    "weight_in_kgs",
                    models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True),
                ),
                ("clinician_initials", models.CharField(max_length=3, null=True)),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Private notes for pharmacist only",
                        max_length=250,
                        null=True,
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
                    "registered_subject",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_pharmacy.registeredsubjectproxy",
                        verbose_name="Subject Identifier",
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
                "verbose_name": "historical rx",
                "verbose_name_plural": "historical rxs",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalSubstitutions",
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
                ("report_datetime", models.DateTimeField()),
                ("row_index", models.IntegerField(null=True)),
                ("sid", models.IntegerField(verbose_name="SID")),
                (
                    "visit_no",
                    models.IntegerField(blank=True, null=True, verbose_name="Visit Number"),
                ),
                ("dispensed_sid", models.IntegerField(verbose_name="Dispensed SID")),
                (
                    "updated_visit_no",
                    models.IntegerField(blank=True, null=True, verbose_name="Visit Number"),
                ),
                (
                    "updated_subject_identifier",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Taken from subject"
                    ),
                ),
                (
                    "arm_match",
                    models.CharField(
                        choices=[
                            ("Yes", "Yes"),
                            ("No", "No"),
                            ("not_evaluated", "Not evaluated"),
                        ],
                        default="not_evaluated",
                        max_length=15,
                    ),
                ),
                ("notes", models.TextField(verbose_name="Notes")),
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
                    "rx",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="meta_pharmacy.rx",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical IMP Substitution",
                "verbose_name_plural": "historical IMP Substitutions",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="Substitutions",
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
                ("report_datetime", models.DateTimeField()),
                ("row_index", models.IntegerField(null=True)),
                ("sid", models.IntegerField(verbose_name="SID")),
                (
                    "visit_no",
                    models.IntegerField(blank=True, null=True, verbose_name="Visit Number"),
                ),
                ("dispensed_sid", models.IntegerField(verbose_name="Dispensed SID")),
                (
                    "updated_visit_no",
                    models.IntegerField(blank=True, null=True, verbose_name="Visit Number"),
                ),
                (
                    "updated_subject_identifier",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Taken from subject"
                    ),
                ),
                (
                    "arm_match",
                    models.CharField(
                        choices=[
                            ("Yes", "Yes"),
                            ("No", "No"),
                            ("not_evaluated", "Not evaluated"),
                        ],
                        default="not_evaluated",
                        max_length=15,
                    ),
                ),
                ("notes", models.TextField(verbose_name="Notes")),
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
                    "rx",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="meta_pharmacy.rx",
                    ),
                ),
            ],
            options={
                "verbose_name": "IMP Substitution",
                "verbose_name_plural": "IMP Substitutions",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "default_manager_name": "objects",
                "indexes": [
                    models.Index(
                        fields=["sid", "dispensed_sid", "subject_identifier"],
                        name="meta_pharma_sid_8172c4_idx",
                    ),
                    models.Index(fields=["row_index"], name="meta_pharma_row_ind_d06d33_idx"),
                ],
            },
            managers=[
                ("objects", meta_pharmacy.models.MyManager()),
                ("on_site", edc_sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
