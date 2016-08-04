from django.db import models
import datetime

# Blueprint for our database

class Reservation(models.Model):
    date = models.DateField(default=datetime.date.today)
    room = models.PositiveSmallIntegerField(default=0)
    ubnumber = models.PositiveSmallIntegerField(default=0)
    period = models.PositiveSmallIntegerField(default=0)

    def to_list(self):
        return [self.room, self.period]

    def __str__(self):
        return str(self.date) + " : UB#" + str(self.ubnumber) + "\tRoom " + str(self.room)
