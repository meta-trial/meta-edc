# Generated by Django 2.2.6 on 2019-10-26 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("meta_lists", "0001_initial")]

    operations = [
        migrations.AlterModelOptions(
            name="arvregimens", options={"ordering": ["display_index", "display_name"]}
        ),
        migrations.AlterModelOptions(
            name="baselinesymptoms",
            options={"ordering": ["display_index", "display_name"]},
        ),
        migrations.AlterModelOptions(
            name="diabetessymptoms",
            options={"ordering": ["display_index", "display_name"]},
        ),
        migrations.AlterModelOptions(
            name="offstudyreasons",
            options={"ordering": ["display_index", "display_name"]},
        ),
        migrations.AlterModelOptions(
            name="oiprophylaxis",
            options={"ordering": ["display_index", "display_name"]},
        ),
        migrations.AlterModelOptions(
            name="symptoms", options={"ordering": ["display_index", "display_name"]}
        ),
        migrations.RemoveIndex(model_name="arvregimens", name="meta_lists__id_10dc52_idx"),
        migrations.RemoveIndex(
            model_name="baselinesymptoms", name="meta_lists__id_5d3e73_idx"
        ),
        migrations.RemoveIndex(
            model_name="diabetessymptoms", name="meta_lists__id_de7534_idx"
        ),
        migrations.RemoveIndex(model_name="offstudyreasons", name="meta_lists__id_d6cb87_idx"),
        migrations.RemoveIndex(model_name="oiprophylaxis", name="meta_lists__id_509dd4_idx"),
        migrations.RemoveIndex(model_name="symptoms", name="meta_lists__id_f12990_idx"),
        migrations.RenameField(
            model_name="arvregimens", old_name="name", new_name="display_name"
        ),
        migrations.RenameField(
            model_name="baselinesymptoms", old_name="name", new_name="display_name"
        ),
        migrations.RenameField(
            model_name="diabetessymptoms", old_name="name", new_name="display_name"
        ),
        migrations.RenameField(
            model_name="offstudyreasons", old_name="name", new_name="display_name"
        ),
        migrations.RenameField(
            model_name="oiprophylaxis", old_name="name", new_name="display_name"
        ),
        migrations.RenameField(
            model_name="symptoms", old_name="name", new_name="display_name"
        ),
        migrations.RenameField(
            model_name="arvregimens", old_name="short_name", new_name="name"
        ),
        migrations.RenameField(
            model_name="baselinesymptoms", old_name="short_name", new_name="name"
        ),
        migrations.RenameField(
            model_name="diabetessymptoms", old_name="short_name", new_name="name"
        ),
        migrations.RenameField(
            model_name="offstudyreasons", old_name="short_name", new_name="name"
        ),
        migrations.RenameField(
            model_name="oiprophylaxis", old_name="short_name", new_name="name"
        ),
        migrations.RenameField(model_name="symptoms", old_name="short_name", new_name="name"),
        migrations.AddIndex(
            model_name="arvregimens",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="meta_lists__id_18210c_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="baselinesymptoms",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="meta_lists__id_5cfb01_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="diabetessymptoms",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="meta_lists__id_9b6cbb_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="offstudyreasons",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="meta_lists__id_713d23_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="oiprophylaxis",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="meta_lists__id_399299_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="symptoms",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="meta_lists__id_1f5296_idx",
            ),
        ),
    ]
