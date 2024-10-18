# Generated by Django 5.1.2 on 2024-10-10 19:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("current_score", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dealer_score", models.IntegerField(default=0)),
                ("player_score", models.IntegerField(default=0)),
                ("game_result", models.CharField(default="", max_length=50)),
                ("deck", models.JSONField()),
                ("player_hand", models.JSONField(default=list)),
                ("dealer_hand", models.JSONField(default=list)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="game.player"
                    ),
                ),
            ],
        ),
    ]
