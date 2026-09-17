"""Carry meta_ae.AeFinalClassification.verified into review_status.

`verified` meant that the two source classifications agreed, which is
what `review_status` now records as `AGREED`. It never meant that a
person had looked at the record, so nothing here sets
`conflict_resolved` to `YES`: that tick is a reviewer's to give, and
`NOT_APPLICABLE` says nobody has yet.

`verified` is dropped in a later migration, once this has run.
"""

from django.db import migrations

# spelled out rather than imported from meta_ae.constants, so that
# renaming a constant later cannot change what this migration did
AGREED = "agreed"
NOT_APPLICABLE = "N/A"


def convert_verified_to_review_status(apps, schema_editor):
    for model_name in ["AeFinalClassification", "HistoricalAeFinalClassification"]:
        model_cls = apps.get_model("meta_ae", model_name)
        model_cls.objects.using(schema_editor.connection.alias).filter(verified=True).update(
            review_status=AGREED, conflict_resolved=NOT_APPLICABLE
        )


def convert_review_status_to_verified(apps, schema_editor):
    for model_name in ["AeFinalClassification", "HistoricalAeFinalClassification"]:
        model_cls = apps.get_model("meta_ae", model_name)
        qs = model_cls.objects.using(schema_editor.connection.alias)
        qs.filter(review_status=AGREED).update(verified=True)
        qs.exclude(review_status=AGREED).update(verified=False)


class Migration(migrations.Migration):
    dependencies = [
        ("meta_ae", "0025_remove_aefinalclassification_verified_and_more"),
    ]

    operations = [
        migrations.RunPython(
            convert_verified_to_review_status,
            convert_review_status_to_verified,
            elidable=False,
        ),
    ]
