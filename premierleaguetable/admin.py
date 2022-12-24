from django.contrib import admin
# this will import the model
from .models import PremierTable

# Register your models here.
# Register your models here.
# this will allow you to add data to the database from the admin page
admin.site.register(PremierTable)