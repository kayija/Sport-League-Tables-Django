from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.views import generic
from .models import PremierTable
from django.contrib import messages
from django.db.models import F


# Create your views here.
# DetailView is for a template that get its data from a model(database)
class TableView(generic.ListView):
    queryset = PremierTable.objects.all()
    template_name = 'index.html'


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
    #updatetable()
    if request.method == 'POST':
        HomeTeam = request.POST['HomeTeam']
        AwayTeam = request.POST['AwayTeam']
        HomeTeamGoals = request.POST['HomeGoals']
        AwayTeamGoals = request.POST['AwayGoals']

        if HomeTeam == AwayTeam:
            messages.error(request, 'Home Team and Away Team can not be the same')
        if HomeTeam == 'Teams' or AwayTeam == 'Teams':
            messages.error(request, 'Home or Away Team not selected')

        if HomeTeamGoals > AwayTeamGoals:
            print(HomeTeam)
            PremierTable.objects.filter(Club=HomeTeam).update(Pts=F('Pts') + 3)

            # # .update(Pts=F('Pts') + 3, MP=F('MP') + 1,)
            # # queryset.Pts = 3

        elif AwayTeamGoals > HomeTeamGoals:
            print("Away Team Won")
        else:
            print("Tie")
            queryset = PremierTable.objects.filter(Club=AwayTeam).update(Pts=F('Pts') + 3, MP=F('MP') + 1,)
            # queryset.Pts = 3

    with open("premier-league.csv") as data:
        file = data.readlines()
        teams = [team.replace('\n', '') for team in file]
        print(teams)

    return render(request, 'fixtures.html', {'teams': teams})


