from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Bus(models.Model):

    bID = models.CharField(primary_key=True, max_length=15)
    busType = models.CharField(max_length=50)
    seats = models.IntegerField()
    costpseat = models.IntegerField(null=True)

    def __str__(self):
        return self.bID


class Route(models.Model):

    rID = models.CharField(primary_key=True, max_length=15)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)

    def __str__(self):
        return self.rID

class AvailableBusRoute(models.Model):

    rID = models.ForeignKey(Route, on_delete=models.CASCADE)
    bID = models.ForeignKey(Bus, on_delete=models.CASCADE)
    jDate = models.DateField()
    jTime = models.TimeField()

    def __str__(self):
        return str(self.jDate)

class BookedTicket(models.Model):

    tID = models.AutoField(primary_key=True,default=None)
    bID = models.ForeignKey(Bus, on_delete=models.CASCADE)
    rID = models.ForeignKey(Route, on_delete=models.CASCADE)
    uID = models.ForeignKey(User, on_delete=models.CASCADE)
    booked = models.IntegerField()
    amount = models.IntegerField(null=True)
    status = models.CharField(max_length=15,null=True)

    def __str__(self):
        return str(self.uID) 