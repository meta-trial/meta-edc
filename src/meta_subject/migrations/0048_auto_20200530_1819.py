from django.db import migrations


def update_subject_visit_metadata(apps, schema_editor):
    subject_visit_model_cls = apps.get_model("meta_subject.subjectvisit")
    for obj in subject_visit_model_cls.objects.all():
        obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ("meta_subject", "0047_auto_20200530_1819"),
    ]

    operations = [migrations.RunPython(update_subject_visit_metadata)]
