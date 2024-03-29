# Generated by Django 5.0 on 2024-01-09 23:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meta_consent", "0018_alter_subjectconsent_options_and_more"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subjectconsent",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "verbose_name": "Subject Consent",
                "verbose_name_plural": "Subject Consents",
            },
        ),
        migrations.RemoveIndex(
            model_name="subjectconsent",
            name="meta_consen_subject_6fdb8c_idx",
        ),
        migrations.AddField(
            model_name="historicalsubjectconsent",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectconsent",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectreconsent",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectreconsent",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="subjectconsent",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="subjectconsent",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="subjectreconsent",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="subjectreconsent",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="language",
            field=models.CharField(
                choices=[
                    ("sw", "Swahili"),
                    ("en-gb", "British English"),
                    ("en", "English"),
                    ("mas", "Maasai"),
                ],
                help_text="The language used for the consent process will also be used during data collection.",
                max_length=25,
                verbose_name="Language of consent",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="language",
            field=models.CharField(
                choices=[
                    ("sw", "Swahili"),
                    ("en-gb", "British English"),
                    ("en", "English"),
                    ("mas", "Maasai"),
                ],
                help_text="The language used for the consent process will also be used during data collection.",
                max_length=25,
                verbose_name="Language of consent",
            ),
        ),
        migrations.AddIndex(
            model_name="subjectconsent",
            index=models.Index(
                fields=["modified", "created"], name="meta_consen_modifie_0437ee_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="subjectconsent",
            index=models.Index(
                fields=["user_modified", "user_created"],
                name="meta_consen_user_mo_b20eb9_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="subjectconsent",
            constraint=models.UniqueConstraint(
                fields=("first_name", "dob", "initials", "version"),
                name="meta_consent_subjectconsent_first_uniq",
            ),
        ),
        migrations.AddConstraint(
            model_name="subjectconsent",
            constraint=models.UniqueConstraint(
                fields=(
                    "subject_identifier",
                    "first_name",
                    "dob",
                    "initials",
                    "version",
                ),
                name="meta_consent_subjectconsent_subject_uniq",
            ),
        ),
        migrations.AddConstraint(
            model_name="subjectconsent",
            constraint=models.UniqueConstraint(
                fields=("version", "subject_identifier"),
                name="meta_consent_subjectconsent_version_uniq",
            ),
        ),
    ]
