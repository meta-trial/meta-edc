# Generated by Django 4.0.5 on 2022-06-29 15:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("meta_prn", "0032_historicalegfrnotification_egfrnotification"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalegfrnotification",
            name="action_item",
        ),
        migrations.RemoveField(
            model_name="historicalegfrnotification",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicalegfrnotification",
            name="parent_action_item",
        ),
        migrations.RemoveField(
            model_name="historicalegfrnotification",
            name="related_action_item",
        ),
        migrations.RemoveField(
            model_name="historicalegfrnotification",
            name="site",
        ),
        migrations.DeleteModel(
            name="EgfrNotification",
        ),
        migrations.DeleteModel(
            name="HistoricalEgfrNotification",
        ),
    ]
