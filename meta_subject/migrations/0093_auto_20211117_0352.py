# Generated by Django 3.2.9 on 2021-11-17 00:52

import _socket
from django.conf import settings
import django.contrib.sites.managers
from django.db import migrations, models
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import edc_model.models.validators.date
import edc_protocol.validators
import edc_utils.date
import edc_visit_tracking.managers
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('edc_pharmacy', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meta_subject', '0092_auto_20211013_0447'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalSf12',
            fields=[
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('created', models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow)),
                ('modified', models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow)),
                ('user_created', django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', django_audit_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.')),
                ('report_datetime', models.DateTimeField(default=edc_utils.date.get_utcnow, help_text="If reporting today, use today's date/time, otherwise use the date/time this information was reported.", validators=[edc_protocol.validators.datetime_not_before_study_start, edc_model.models.validators.date.datetime_not_future], verbose_name='Report Date')),
                ('consent_model', models.CharField(editable=False, max_length=50, null=True)),
                ('consent_version', models.CharField(editable=False, max_length=10, null=True)),
                ('general_health', models.CharField(choices=[('excellent', 'Excellent'), ('very_good', 'Very good'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')], max_length=15, verbose_name='In general, would you say your health is:')),
                ('moderate_activities_now_limited', models.CharField(choices=[('limited_a_lot', 'YES, limited a lot'), ('limited_a_little', 'YES, limited a little'), ('not_limited_at_all', 'NO, not at all limited')], max_length=20, verbose_name='<u>Moderate activities</u> such as moving a table, pushing a vacuum cleaner, bowling, or playing golf:')),
                ('climbing_stairs_now_limited', models.CharField(choices=[('limited_a_lot', 'YES, limited a lot'), ('limited_a_little', 'YES, limited a little'), ('not_limited_at_all', 'NO, not at all limited')], max_length=20, verbose_name='Climbing <u>several</u> flights of stairs:')),
                ('accomplished_less_physical_health', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, verbose_name='<u>Accomplished less</u> than you would like:')),
                ('work_limited_physical_health', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, verbose_name='Were limited in the <u>kind</u> of work or other activities:')),
                ('accomplished_less_emotional', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, verbose_name='<u>Accomplished less</u> than you would like:')),
                ('work_less_carefully_emotional', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, verbose_name='Did work or activities <u>less carefully than usual</u>:')),
                ('pain_interfere_work', models.CharField(choices=[('not_at_all', 'Not at all'), ('a_little_bit', 'A little bit'), ('moderately', 'Moderately'), ('quite_a-bit', 'Quite a bit'), ('extremely', 'Extremely')], max_length=15, verbose_name='During the <u>past 4 weeks</u>, how much <u>did pain interfere</u> with your normal work (including work outside the home and housework)?')),
                ('felt_calm_peaceful', models.CharField(choices=[('all_of_the_time', 'All of the time'), ('most_of_the_time', 'Most of the time'), ('good_bit_of_the_time', ' A good bit of the time'), ('some_of_the_time', 'Some of the time'), ('little_of_the_time', 'A little of the time'), ('none_of_the_time', 'None of the time')], max_length=25, verbose_name='Have you felt calm & peaceful?')),
                ('felt_lot_energy', models.CharField(choices=[('all_of_the_time', 'All of the time'), ('most_of_the_time', 'Most of the time'), ('good_bit_of_the_time', ' A good bit of the time'), ('some_of_the_time', 'Some of the time'), ('little_of_the_time', 'A little of the time'), ('none_of_the_time', 'None of the time')], max_length=25, verbose_name='Did you have a lot of energy?')),
                ('felt_down', models.CharField(choices=[('all_of_the_time', 'All of the time'), ('most_of_the_time', 'Most of the time'), ('good_bit_of_the_time', ' A good bit of the time'), ('some_of_the_time', 'Some of the time'), ('little_of_the_time', 'A little of the time'), ('none_of_the_time', 'None of the time')], max_length=25, verbose_name='Have you felt down-hearted and blue?')),
                ('social_activities_interfered', models.CharField(choices=[('all_of_the_time', 'All of the time'), ('most_of_the_time', 'Most of the time'), ('some_of_the_time', 'Some of the time'), ('little_of_the_time', 'A little of the time'), ('none_of_the_time', 'None of the time')], max_length=25, verbose_name='During the <u>past 4 weeks</u>, how much of the time has your physical health or emotional problems interfered with your social activities (like visiting friends, relatives, etc.)?')),
                ('crf_status', models.CharField(choices=[('INCOMPLETE', 'Incomplete (some data pending)'), ('COMPLETE', 'Complete')], default='COMPLETE', help_text='If some data is still pending, flag this CRF as incomplete', max_length=25, verbose_name='CRF status')),
                ('crf_status_comments', models.TextField(blank=True, help_text='for example, why some data is still pending', null=True, verbose_name='Any comments related to status of this CRF')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical SF-12 Health Survey',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Sf12',
            fields=[
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('created', models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow)),
                ('modified', models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow)),
                ('user_created', django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', django_audit_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('report_datetime', models.DateTimeField(default=edc_utils.date.get_utcnow, help_text="If reporting today, use today's date/time, otherwise use the date/time this information was reported.", validators=[edc_protocol.validators.datetime_not_before_study_start, edc_model.models.validators.date.datetime_not_future], verbose_name='Report Date')),
                ('consent_model', models.CharField(editable=False, max_length=50, null=True)),
                ('consent_version', models.CharField(editable=False, max_length=10, null=True)),
                ('general_health', models.CharField(choices=[('excellent', 'Excellent'), ('very_good', 'Very good'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')], max_length=15, verbose_name='In general, would you say your health is:')),
                ('moderate_activities_now_limited', models.CharField(choices=[('limited_a_lot', 'YES, limited a lot'), ('limited_a_little', 'YES, limited a little'), ('not_limited_at_all', 'NO, not at all limited')], max_length=20, verbose_name='<u>Moderate activities</u> such as moving a table, pushing a vacuum cleaner, bowling, or playing golf:')),
                ('climbing_stairs_now_limited', models.CharField(choices=[('limited_a_lot', 'YES, limited a lot'), ('limited_a_little', 'YES, limited a little'), ('not_limited_at_all', 'NO, not at all limited')], max_length=20, verbose_name='Climbing <u>several</u> flights of stairs:')),
                ('accomplished_less_physical_health', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, verbose_name='<u>Accomplished less</u> than you would like:')),
                ('work_limited_physical_health', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, verbose_name='Were limited in the <u>kind</u> of work or other activities:')),
                ('accomplished_less_emotional', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, verbose_name='<u>Accomplished less</u> than you would like:')),
                ('work_less_carefully_emotional', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, verbose_name='Did work or activities <u>less carefully than usual</u>:')),
                ('pain_interfere_work', models.CharField(choices=[('not_at_all', 'Not at all'), ('a_little_bit', 'A little bit'), ('moderately', 'Moderately'), ('quite_a-bit', 'Quite a bit'), ('extremely', 'Extremely')], max_length=15, verbose_name='During the <u>past 4 weeks</u>, how much <u>did pain interfere</u> with your normal work (including work outside the home and housework)?')),
                ('felt_calm_peaceful', models.CharField(choices=[('all_of_the_time', 'All of the time'), ('most_of_the_time', 'Most of the time'), ('good_bit_of_the_time', ' A good bit of the time'), ('some_of_the_time', 'Some of the time'), ('little_of_the_time', 'A little of the time'), ('none_of_the_time', 'None of the time')], max_length=25, verbose_name='Have you felt calm & peaceful?')),
                ('felt_lot_energy', models.CharField(choices=[('all_of_the_time', 'All of the time'), ('most_of_the_time', 'Most of the time'), ('good_bit_of_the_time', ' A good bit of the time'), ('some_of_the_time', 'Some of the time'), ('little_of_the_time', 'A little of the time'), ('none_of_the_time', 'None of the time')], max_length=25, verbose_name='Did you have a lot of energy?')),
                ('felt_down', models.CharField(choices=[('all_of_the_time', 'All of the time'), ('most_of_the_time', 'Most of the time'), ('good_bit_of_the_time', ' A good bit of the time'), ('some_of_the_time', 'Some of the time'), ('little_of_the_time', 'A little of the time'), ('none_of_the_time', 'None of the time')], max_length=25, verbose_name='Have you felt down-hearted and blue?')),
                ('social_activities_interfered', models.CharField(choices=[('all_of_the_time', 'All of the time'), ('most_of_the_time', 'Most of the time'), ('some_of_the_time', 'Some of the time'), ('little_of_the_time', 'A little of the time'), ('none_of_the_time', 'None of the time')], max_length=25, verbose_name='During the <u>past 4 weeks</u>, how much of the time has your physical health or emotional problems interfered with your social activities (like visiting friends, relatives, etc.)?')),
                ('crf_status', models.CharField(choices=[('INCOMPLETE', 'Incomplete (some data pending)'), ('COMPLETE', 'Complete')], default='COMPLETE', help_text='If some data is still pending, flag this CRF as incomplete', max_length=25, verbose_name='CRF status')),
                ('crf_status_comments', models.TextField(blank=True, help_text='for example, why some data is still pending', null=True, verbose_name='Any comments related to status of this CRF')),
            ],
            options={
                'verbose_name': 'SF-12 Health Survey',
                'verbose_name_plural': 'SF-12 Health Survey',
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view', 'export', 'import'),
            },
            managers=[
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
                ('objects', edc_visit_tracking.managers.CrfModelManager()),
            ],
        ),
        migrations.AddField(
            model_name='historicalpatienthistory',
            name='previous_arv_regimen_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='When did the patient start this previous antiretroviral therapy regimen?'),
        ),
        migrations.AddField(
            model_name='historicalstudymedication',
            name='dosage_guideline',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_pharmacy.dosageguideline'),
        ),
        migrations.AddField(
            model_name='historicalstudymedication',
            name='formulation',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_pharmacy.formulation'),
        ),
        migrations.AddField(
            model_name='historicalstudymedication',
            name='next_dosage_guideline',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_pharmacy.dosageguideline'),
        ),
        migrations.AddField(
            model_name='historicalstudymedication',
            name='next_formulation',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_pharmacy.formulation'),
        ),
        migrations.AddField(
            model_name='historicalstudymedication',
            name='number_of_days',
            field=models.IntegerField(blank=True, help_text='Leave blank to auto-calculate relative to the next scheduled appointment', null=True),
        ),
        migrations.AddField(
            model_name='historicalstudymedication',
            name='order_next',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=15, verbose_name='Order medication for next visit?'),
        ),
        migrations.AddField(
            model_name='historicalstudymedication',
            name='special_instructions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patienthistory',
            name='previous_arv_regimen_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='When did the patient start this previous antiretroviral therapy regimen?'),
        ),
        migrations.AddField(
            model_name='studymedication',
            name='dosage_guideline',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='edc_pharmacy.dosageguideline'),
        ),
        migrations.AddField(
            model_name='studymedication',
            name='formulation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='edc_pharmacy.formulation'),
        ),
        migrations.AddField(
            model_name='studymedication',
            name='next_dosage_guideline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='next_dosageguideline', to='edc_pharmacy.dosageguideline'),
        ),
        migrations.AddField(
            model_name='studymedication',
            name='next_formulation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='next_formulation', to='edc_pharmacy.formulation'),
        ),
        migrations.AddField(
            model_name='studymedication',
            name='number_of_days',
            field=models.IntegerField(blank=True, help_text='Leave blank to auto-calculate relative to the next scheduled appointment', null=True),
        ),
        migrations.AddField(
            model_name='studymedication',
            name='order_next',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=15, verbose_name='Order medication for next visit?'),
        ),
        migrations.AddField(
            model_name='studymedication',
            name='special_instructions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='eq5d3l',
            index=models.Index(fields=['subject_visit', 'site', 'id'], name='meta_subjec_subject_554b24_idx'),
        ),
        migrations.AddField(
            model_name='sf12',
            name='site',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='sites.site'),
        ),
        migrations.AddField(
            model_name='sf12',
            name='subject_visit',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='meta_subject.subjectvisit'),
        ),
        migrations.AddField(
            model_name='historicalsf12',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalsf12',
            name='site',
            field=models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sites.site'),
        ),
        migrations.AddField(
            model_name='historicalsf12',
            name='subject_visit',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meta_subject.subjectvisit'),
        ),
        migrations.AddIndex(
            model_name='sf12',
            index=models.Index(fields=['subject_visit', 'site', 'id'], name='meta_subjec_subject_6b795b_idx'),
        ),
    ]
