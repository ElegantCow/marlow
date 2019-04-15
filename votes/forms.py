from django import forms
from django.contrib.auth.models import User
from . import models

users = User.objects.all()
players = []
for user in users:
    players.append((user.first_name+' '+user.last_name,user.first_name+' '+user.last_name))

class PlayerVotesForm(forms.ModelForm):
    class Meta:
        model = models.PlayerVotes
        fields = ('three_votes', 'two_votes', 'one_vote')


    def __init__(self, user, round, *args, **kwargs):
        self.voter = user
        self.round = round
        super(PlayerVotesForm, self).__init__(*args, **kwargs)

    def clean(self):
        all_clean_data = super().clean()
        three_votes = all_clean_data.get('three_votes')
        two_votes = all_clean_data.get('two_votes')
        one_vote = all_clean_data.get('one_vote')

        if three_votes == two_votes or three_votes == one_vote or two_votes == one_vote:
            raise forms.ValidationError('You cannot vote for the same person more than once.')
        if self.voter == three_votes or self.voter == two_votes or self.voter == one_vote:
            raise forms.ValidationError('You cannot vote for yourself!')


    def save(self):
        player_votes = super(PlayerVotesForm, self).save(commit=False)
        player_votes.voter = self.voter
        player_votes.round = self.round
        player_votes.save()
        return player_votes
