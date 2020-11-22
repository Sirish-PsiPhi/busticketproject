from django.db import models

# Create your models here.
class Bus(models.Model):

    bID = models.CharField(primary_key=True, max_length=15)
    busType = models.CharField(max_length=50)
    seats = models.IntegerField()


class Route(models.Model):

    rID = models.CharField(primary_key=True, max_length=15)
    bID = models.ForeignKey(Bus, on_delete=models.CASCADE)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    jDate = models.DateField()
    jTime = models.TimeField()
