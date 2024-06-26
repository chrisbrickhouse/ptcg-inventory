# Generated by Django 5.0.4 on 2024-05-13 19:23

from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0003_populate_uuid_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='deck_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
