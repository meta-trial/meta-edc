# Generated by Django 3.0.6 on 2020-05-30 15:01

import uuid

import _socket
import django.contrib.sites.managers
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
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
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sites", "0002_alter_domain_unique"),
        ("meta_lists", "0008_auto_20200528_1517"),
        ("edc_action_item", "0025_auto_20200528_0520"),
        ("meta_subject", "0044_auto_20200528_1853"),
    ]

    operations = [
        migrations.RenameModel(old_name="Followup", new_name="FollowupExamination"),
        migrations.RenameModel(
            old_name="HistoricalFollowup", new_name="HistoricalFollowupExamination"
        ),
    ]
