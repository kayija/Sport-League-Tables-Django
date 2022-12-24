from django.db import models


# Create your models here.
class PremierTable(models.Model):
    Club = models.CharField(max_length=200, unique=True)
    MP = models.IntegerField(default=0)
    W = models.IntegerField(default=0)
    D = models.IntegerField(default=0)
    L = models.IntegerField(default=0)
    GF = models.IntegerField(default=0)
    GA = models.IntegerField(default=0)
    GD = models.IntegerField(default=0)
    Pts = models.IntegerField(default=0)

    # this will return the actual name of the model object
    def __str__(self):
        return self.Club

