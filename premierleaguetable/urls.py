from . import views
from django.urls import path

urlpatterns = [
    path('', views.TableView.as_view(), name='Home'),
    path('fixtures/', views.fixtures_view, name='fixtures')
]
