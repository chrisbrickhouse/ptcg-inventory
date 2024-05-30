# Generated by Django 5.0.4 on 2024-05-22 21:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0012_rename_card_id_cardallocation_card_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='is_stash',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deck',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='date modified'),
        ),
    ]