from django.db import models

class Player(models.Model):
    name            = models.CharField(max_length=100)
    current_score   = models.IntegerField(default=0)

class Game(models.Model):
    player          = models.ForeignKey(Player, on_delete=models.CASCADE)
    dealer_score    = models.IntegerField(default=0)
    player_score    = models.IntegerField(default=0)
    game_result     = models.CharField(max_length=50, default='')
    deck            = models.JSONField()
    player_hand     = models.JSONField(default=list)
    dealer_hand     = models.JSONField(default=list)
    is_active       = models.BooleanField(default=True)
