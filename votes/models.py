from django.db import models
from django.core.validators  import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from datetime import datetime
from django.contrib import auth
# Create your models here.

# Create your models here.
User = get_user_model()

class Teams(models.Model):
    team_name = models.CharField("Team Name", max_length=255)

    def __str__(self):
        return self.team_name

class Fixture(models.Model):
    season = models.PositiveIntegerField(blank=False, null=False,
            validators=[
                MinValueValidator(2019),
                MaxValueValidator(datetime.now().year)])
    round = models.PositiveIntegerField(blank=False, null=False)
    game_time = models.DateTimeField(blank=True, null=True)
    opponent = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True)
    goals_for = models.PositiveIntegerField(null=True)
    goals_againt = models.PositiveIntegerField(null=True)

    def __str__(self):
        return 'Round '+str(self.round)+ ' ('+str(self.season)+ ')'

class PlayerVotes(models.Model):
    voter = models.ForeignKey(User,related_name="voter" ,on_delete=models.SET_NULL, null=True)
    round = models.ForeignKey(Fixture, on_delete=models.SET_NULL, null=True)
    three_votes = models.ForeignKey(User,related_name="three_votes" ,on_delete=models.SET_NULL, null=True)
    two_votes = models.ForeignKey(User,related_name="two_votes" ,on_delete=models.SET_NULL, null=True)
    one_vote = models.ForeignKey(User,related_name="one_vote", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.voter) + '('+str(self.round) + ')'
