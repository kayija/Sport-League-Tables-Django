from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.views import generic
from .models import PremierTable
from django.contrib import messages
from django.db.models import F


# Create your views here.
# DetailView is for a template that get its data from a model(database)
class TableView(generic.ListView):
    # This will order the table by Pts first then by Goal difference if a team has the same points.
    queryset = PremierTable.objects.all().order_by("-Pts", "-GD").values()
    template_name = 'index.html'


# This function will pull data from the csv file and add it to the database
def updatetable():
    with open("premier-league.csv") as data:
        file = data.readlines()
        teams = [team.replace('\n', '') for team in file]

    for team in teams:
        if team == 'Teams':
            pass
        else:
            a = PremierTable(Club=team)
            a.save()


# a decorator to prevent ordinary users from accessing the fixtures page
def admin_check(user):
    return user.is_superuser


# view for the fixtures page
@user_passes_test(admin_check)
def fixtures_view(request):
    # updatetable()
    if request.method == 'POST':
        HomeTeam = request.POST['HomeTeam']
        AwayTeam = request.POST['AwayTeam']
        HomeTeamGoals = int(request.POST['HomeGoals'])
        AwayTeamGoals = int(request.POST['AwayGoals'])

        if HomeTeam == AwayTeam:
            messages.error(request, 'Home Team and Away Team can not be the same')
        if HomeTeam == 'Teams' or AwayTeam == 'Teams':
            messages.error(request, 'Home or Away Team not selected')

        # Home Teams Wins
        if HomeTeamGoals > AwayTeamGoals:
            PremierTable.objects.filter(Club=HomeTeam).update(MP=F('MP') + 1, W=F('W') + 1,
                                                              GF=F('GF') + HomeTeamGoals, GA=F('GA') + AwayTeamGoals,
                                                              GD=F('GD') + (HomeTeamGoals - AwayTeamGoals),
                                                              Pts=F('Pts') + 3)
            PremierTable.objects.filter(Club=AwayTeam).update(MP=F('MP') + 1, L=F('L') + 1,
                                                              GF=F('GF') + AwayTeamGoals, GA=F('GA') + HomeTeamGoals,
                                                              GD=F('GD') + (AwayTeamGoals - HomeTeamGoals))
        # Away Team Wins
        elif AwayTeamGoals > HomeTeamGoals:
            PremierTable.objects.filter(Club=AwayTeam).update(MP=F('MP') + 1, W=F('W') + 1,
                                                              GF=F('GF') + AwayTeamGoals, GA=F('GA') + HomeTeamGoals,
                                                              GD=F('GD') + (AwayTeamGoals - HomeTeamGoals),
                                                              Pts=F('Pts') + 3)
        # Tie
        else:
            PremierTable.objects.filter(Club=HomeTeam).update(MP=F('MP') + 1, D=F('D') + 1,
                                                              GF=F('GF') + HomeTeamGoals, GA=F('GA') + AwayTeamGoals,
                                                              GD=F('GD') + (HomeTeamGoals - AwayTeamGoals),
                                                              Pts=F('Pts') + 1)
            PremierTable.objects.filter(Club=AwayTeam).update(MP=F('MP') + 1, D=F('D') + 1,
                                                              GF=F('GF') + AwayTeamGoals, GA=F('GA') + HomeTeamGoals,
                                                              GD=F('GD') + (AwayTeamGoals - HomeTeamGoals),
                                                              Pts=F('Pts') + 1)
    # this will autopopulate the dropdown for the admin to use to add the teams
    with open("premier-league.csv") as data:
        file = data.readlines()
        teams = [team.replace('\n', '') for team in file]

    return render(request, 'fixtures.html', {'teams': teams})


