from . import views
from django.urls import path

urlpatterns = [
    # url for home
    path('', views.TableView.as_view(), name='Home'),
    # url for fixtures
    path('fixtures/', views.fixtures_view, name='fixtures')
]
