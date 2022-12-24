from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import PremierTable
from django.views import generic
from .models import PremierTable


# Create your views here.
# DetailView is for a template that get its data from a model(database)
class TableView(generic.ListView):
    queryset = PremierTable.objects.all()
    template_name = 'index.html'


# a decorator to prevent ordinary users from accessing the fixtures page
def admin_check(user):
    return user.is_superuser


# view for the fixtures page
@user_passes_test(admin_check)
def fixtures_view(request):
    return render(request, template_name='fixtures.html')


