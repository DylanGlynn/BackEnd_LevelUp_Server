from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=99)
    maker = models.CharField(max_length=255)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
    type = models.ForeignKey('GameType', on_delete=models.CASCADE, related_name='games')
