from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import models
from . import forms
from datetime import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from operator import itemgetter

# Create your views here.

def get_full_name(self):
    return self.first_name+' '+self.last_name

User.add_to_class("__str__", get_full_name)


@login_required
def votes(request, form_failed = None):
    fixtures = models.Fixture.objects.filter(season=datetime.today().year) #get all the fixtures for the current year
    games = {}
    for game in fixtures:
        if models.PlayerVotes.objects.filter(voter=request.user, round=game).exists(): #if player has already voted
            status = 'Y'
        else:
            status = 'N'
        games[game] = [forms.PlayerVotesForm(user=request.user, round=game), status] #save voting form
    if form_failed is None: #if there are no errors coming back
        return render(request, 'votes/display.html', context={'games':games, 'failed': None} )
    else: #render form with errors
        return render(request, 'votes/display.html', context={'games':games, 'failed': form_failed} )

@login_required
def cast_vote(request, pk):
    game = get_object_or_404(models.Fixture, pk=pk)
    form_failed = {}
    if request.method == "POST":
        form = forms.PlayerVotesForm(request.user, game,request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('votes:votepage'))
        else:
            form_failed[game] = form.errors
            return votes(request, form_failed)

@staff_member_required
def not_voted(request):
    games={}
    for game in models.Fixture.objects.filter(season=datetime.today().year):
        not_voted = []
        for user in User.objects.all():
            if not models.PlayerVotes.objects.filter(voter=user,round=game):
                not_voted.append(user)
        games[game] = not_voted
    return render(request, 'votes/not_voted.html', {'games':games})


@staff_member_required
def weekly_results(request):
    fixtures = models.Fixture.objects.filter(season=datetime.today().year) #get all the fixtures for the current year
    votes = ['three_votes','two_votes','one_vote']
    games = {}
    for game in fixtures:
        temp_dict = {}
        temp_list = []
        for count, vts in enumerate(votes):
            vote=models.PlayerVotes.objects.filter(round=game).values(vts).annotate(Count(vts))
            for each in vote:
                if each[vts] in temp_dict.keys():
                    temp_dict[each[vts]][count] =  temp_dict[each[vts]][count] + each[str(vts)+"__count"]
                else:
                    if count == 0:
                        temp_dict[each[vts]] = [each[str(vts)+"__count"],0,0]
                    elif count ==1:
                        temp_dict[each[vts]] = [0,each[str(vts)+"__count"],0]
                    else:
                        temp_dict[each[vts]] = [0,0,each[str(vts)+"__count"]]

        for key in temp_dict.keys():

            temp_list.append([User.objects.get(pk=key), int(temp_dict[key][0])*3+int(temp_dict[key][1])*2+int(temp_dict[key][2])*1])

        games[game] = sorted(temp_list, key=itemgetter(1), reverse=True)
    return render(request, 'votes/weekly_results.html', {'games':games})

@staff_member_required
def cumulative_results(request):
    fixtures = models.Fixture.objects.filter(season=datetime.today().year) #get all the fixtures for the current year
    votes = ['three_votes','two_votes','one_vote']
    running_count = {}
    games = {}
    for game in fixtures:
        temp_dict = {}
        temp_list = []
        for count, vts in enumerate(votes):
            vote=models.PlayerVotes.objects.filter(round=game).values(vts).annotate(Count(vts))
            for each in vote:
                if each[vts] in temp_dict.keys():
                    temp_dict[each[vts]][count] =  temp_dict[each[vts]][count] + each[str(vts)+"__count"]
                else:
                    if count == 0:
                        temp_dict[each[vts]] = [each[str(vts)+"__count"],0,0]
                    elif count ==1:
                        temp_dict[each[vts]] = [0,each[str(vts)+"__count"],0]
                    else:
                        temp_dict[each[vts]] = [0,0,each[str(vts)+"__count"]]


        for key in temp_dict.keys():

            temp_list.append([User.objects.get(pk=key), int(temp_dict[key][0])*3+int(temp_dict[key][1])*2+int(temp_dict[key][2])*1])

        for data in temp_list:
            if data[0] in running_count.keys():
                running_count[data[0]] = running_count[data[0]]  + data[1]
            else:
                running_count[data[0]] = data[1]
        list_running_counter = [[k,v] for k,v in running_count.items()]

        games[game] = sorted(list_running_counter, key=itemgetter(1), reverse=True)
    return render(request, 'votes/cumulative_results.html', {'games':games})
