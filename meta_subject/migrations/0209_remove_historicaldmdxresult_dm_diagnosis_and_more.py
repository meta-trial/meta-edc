# Generated by Django 5.0.8 on 2024-08-21 13:45

import uuid

import _socket
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
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0208_birthoutcomes_crf_status_and_more"),
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="historicaldmdiagnosis",
            new_name="historicaldmendpoint",
        ),
        migrations.RenameModel(old_name="dmdiagnosis", new_name="dmendpoint"),
    ]
