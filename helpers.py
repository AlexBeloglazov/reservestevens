import datetime
from book.models import Reservation
from django.db.models import Q

MAX_DAYS = 2

def calc_day(d):
    MAX_HOUR = 16
    today = datetime.date.today()
    if today.weekday() < 4 and datetime.datetime.now().hour >= MAX_HOUR:
        d = d + 1
    if today.weekday() == 4:
        d = (d + d*2) if datetime.datetime.now().hour < MAX_HOUR else (d + 3)
    elif today.weekday() == 5:
        d = d + 2
    elif today.weekday() == 6:
        d = d + 1
    return today + datetime.timedelta(days=d)

# returns list of reservations in form [[day[0,1], room[0,1,2], period[0,1,2,3,4]], ...] for given UB# as integer
def get_reserved(ub_number):
    reserved = []
    for i in range(MAX_DAYS):
        day = Reservation.objects.filter(date=calc_day(i).isoformat(), ubnumber=ub_number)
        for reserv in day:
            it = [i]
            it.extend(reserv.to_list())
            reserved.append(it)
    return reserved
