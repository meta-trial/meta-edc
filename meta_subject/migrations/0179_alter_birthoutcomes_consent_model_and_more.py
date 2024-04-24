# Generated by Django 4.2.10 on 2024-03-07 23:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_lists", "0017_complications_dmmedications_dmtreatments_and_more"),
        ("meta_subject", "0178_historicalhealtheconomicsupdate_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="birthoutcomes",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="birthoutcomes",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsfbc",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsfbc",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultshba1c",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultshba1c",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsins",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsins",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultslft",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultslft",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultslipid",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultslipid",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsrft",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsrft",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="complications",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="complications",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="complicationsglycemia",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="complicationsglycemia",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="concomitantmedication",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="concomitantmedication",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="dietandlifestyle",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="dietandlifestyle",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="dmreferralfollowup",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="dmreferralfollowup",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="dmreferralfollowup",
            name="dm_medications",
            field=models.ManyToManyField(
                blank=True,
                to="meta_lists.dmmedications",
                verbose_name="If 'Yes', please indicate which diabetes drug treatments you are currently taking.",
            ),
        ),
        migrations.AlterField(
            model_name="dmreferralfollowup",
            name="dm_medications_init_date",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="If 'Yes', please give the date when drug treatment was started.",
            ),
        ),
        migrations.AlterField(
            model_name="dmreferralfollowup",
            name="facility_attended",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="If 'Yes', please give the name of the facility you attended",
            ),
        ),
        migrations.AlterField(
            model_name="dmreferralfollowup",
            name="investigations",
            field=models.ManyToManyField(
                blank=True,
                to="meta_lists.investigations",
                verbose_name="If 'Yes', please indicate what investigations were conducted.",
            ),
        ),
        migrations.AlterField(
            model_name="egfrdropnotification",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="egfrdropnotification",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="eq5d3l",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="eq5d3l",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="followupexamination",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="followupexamination",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="followupvitals",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="followupvitals",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="glucose",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="glucose",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="glucosefbg",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="glucosefbg",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="healtheconomics",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="healtheconomics",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="healtheconomicssimple",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="healtheconomicssimple",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="healtheconomicsupdate",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="healtheconomicsupdate",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="healtheconomicsupdate",
            name="external_dependents",
            field=models.IntegerField(
                help_text="Insert '0' if no dependents other than the members in the household roster",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
                verbose_name="Outside of this household, how many other people depend on this household's income?",
            ),
        ),
        migrations.AlterField(
            model_name="hepatitistest",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="hepatitistest",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbirthoutcomes",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbirthoutcomes",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsfbc",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsfbc",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultshba1c",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultshba1c",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsins",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsins",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultslft",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultslft",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultslipid",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultslipid",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsrft",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsrft",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalcomplications",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalcomplications",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalcomplicationsglycemia",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalcomplicationsglycemia",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalconcomitantmedication",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalconcomitantmedication",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldelivery",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldelivery",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldietandlifestyle",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldietandlifestyle",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldmreferralfollowup",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldmreferralfollowup",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldmreferralfollowup",
            name="dm_medications_init_date",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="If 'Yes', please give the date when drug treatment was started.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldmreferralfollowup",
            name="facility_attended",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="If 'Yes', please give the name of the facility you attended",
            ),
        ),
        migrations.AlterField(
            model_name="historicalegfrdropnotification",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalegfrdropnotification",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicaleq5d3l",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicaleq5d3l",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalfollowupexamination",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalfollowupexamination",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalfollowupvitals",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalfollowupvitals",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalglucose",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalglucose",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalglucosefbg",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalglucosefbg",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomics",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomics",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicssimple",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicssimple",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsupdate",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsupdate",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsupdate",
            name="external_dependents",
            field=models.IntegerField(
                help_text="Insert '0' if no dependents other than the members in the household roster",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
                verbose_name="Outside of this household, how many other people depend on this household's income?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhepatitistest",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalhepatitistest",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalmalariatest",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalmalariatest",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalmedicationadherence",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalmedicationadherence",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalotherarvregimens",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalotherarvregimens",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalphysicalexam",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalphysicalexam",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalpregnancyupdate",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalpregnancyupdate",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalsf12",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalsf12",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalstudymedication",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalstudymedication",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalsubjectrequisition",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalsubjectrequisition",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisitmissed",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisitmissed",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalurinedipsticktest",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalurinedipsticktest",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="historicalurinepregnancy",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalurinepregnancy",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="malariatest",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="malariatest",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="medicationadherence",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="medicationadherence",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="otherarvregimens",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="otherarvregimens",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="pregnancyupdate",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="pregnancyupdate",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="sf12",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="sf12",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="studymedication",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="studymedication",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="subjectrequisition",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="subjectrequisition",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="subjectvisitmissed",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="subjectvisitmissed",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="urinedipsticktest",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="urinedipsticktest",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="urinepregnancy",
            name="consent_model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="urinepregnancy",
            name="consent_version",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]