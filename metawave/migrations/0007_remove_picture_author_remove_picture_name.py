# Generated by Django 4.2.6 on 2023-11-03 07:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("metawave", "0006_musiclist_delete_metawavepicture"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="picture",
            name="author",
        ),
        migrations.RemoveField(
            model_name="picture",
            name="name",
        ),
    ]
