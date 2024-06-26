# Generated by Django 5.0.4 on 2024-05-16 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0005_switch_to_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='deck_name',
            field=models.CharField(help_text='A memorable name for the deck.', max_length=80),
        ),
        migrations.AlterField(
            model_name='deck',
            name='game_format',
            field=models.CharField(choices=[('STD', 'Standard'), ('EXP', 'Expanded'), ('GLC', 'Gym Leader Challenge'), ('UNL', 'Unlimited')], help_text='The format this deck is legal in.', max_length=10),
        ),
    ]
