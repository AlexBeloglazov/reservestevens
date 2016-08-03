from django.db import models
import datetime

# Blueprint for our database

class Reservation(models.Model):
    date = models.DateField(default=datetime.date.today)
    room = models.PositiveSmallIntegerField(default=0)
    period1 = models.PositiveSmallIntegerField(default=0)
    period2 = models.PositiveSmallIntegerField(default=0)
    period3 = models.PositiveSmallIntegerField(default=0)
    period4 = models.PositiveSmallIntegerField(default=0)
    period5 = models.PositiveSmallIntegerField(default=0)

    def to_list(self):
        return [self.period1, self.period2, self.period3, self.period4, self.period5]

    def reserve(self, period, ubnumber):
        if period == 0:
            if self.period1:
                return False
            self.period1 = ubnumber
            self.save()
            return True
        if period == 1:
            if self.period2:
                return False
            self.period2 = ubnumber
            self.save()
            return True
        if period == 2:
            if self.period3:
                return False
            self.period3 = ubnumber
            self.save()
            return True
        if period == 3:
            if self.period4:
                return False
            self.period4 = ubnumber
            self.save()
            return True
        if period == 4:
            if self.period5:
                return False
            self.period5 = ubnumber
            self.save()
            return True

    def __str__(self):
        return str(self.date) + " : room #" + str(self.room)
