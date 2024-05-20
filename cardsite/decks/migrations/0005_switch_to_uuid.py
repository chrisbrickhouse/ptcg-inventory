# Generated by Django 5.0.4 on 2024-05-13 19:42

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0004_enforce_unique_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='deck_id',
        ),
        migrations.AlterField(
            model_name='deck',
            name='card_list',
            field=models.ManyToManyField(related_name='deck_uuid', to='decks.card'),
        ),
        migrations.AlterField(
            model_name='deck',
            name='deck_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]