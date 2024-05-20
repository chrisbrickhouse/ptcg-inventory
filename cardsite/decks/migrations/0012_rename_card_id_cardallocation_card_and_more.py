# Generated by Django 5.0.4 on 2024-05-16 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0011_remove_deck_card_list_deck_card_allocation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardallocation',
            old_name='card_id',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='cardallocation',
            old_name='deck_id',
            new_name='deck',
        ),
        migrations.AddConstraint(
            model_name='cardallocation',
            constraint=models.UniqueConstraint(fields=('deck_id', 'card_id'), name='unique_deck_entries'),
        ),
    ]
