# Generated by Django 5.0.4 on 2024-05-13 19:23

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='deck_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='deck',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False, verbose_name='date created'),
        ),
    ]
