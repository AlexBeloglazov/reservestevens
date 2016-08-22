from django.db import models
from django.contrib.auth.models import User
import datetime

# Blueprint for our databases


# Django's user model expansion. Adding another field "ubnumber"
class UBStudent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, to_field='username')
    ubnumber = models.PositiveSmallIntegerField(default=0, primary_key=True)

    def __str__(self):
        return str(self.ubnumber)


class Reservation(models.Model):
    date = models.DateField(default=datetime.date.today)
    room = models.PositiveSmallIntegerField(default=0)
    ubnumber = models.ForeignKey(UBStudent, on_delete=models.CASCADE)
    period = models.PositiveSmallIntegerField(default=0)

    def to_list(self):
        return [self.room, self.period]

    def __str__(self):
        return str(self.date) + " : UB#" + str(self.ubnumber) + "\tRoom " + str(self.room)
