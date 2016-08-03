import datetime
from book.models import Reservation
from django.db.models import Q

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

# returns list of reservations in form [[day[0,1], room[1,2,3], period[1,2,3,4,5]], ...] for given UB# as integer
def get_reserved(ub_number):
    days = [Reservation.objects.filter(Q(date=calc_day(i).isoformat()), Q(period1=ub_number) | Q(period2=ub_number) |
            Q(period3=ub_number) | Q(period4=ub_number) | Q(period5=ub_number)) for i in range(2)]
    reserved = []
    for i,day in enumerate(days):
        if len(day):
            for reserv in day:
                for j,reserved_by in enumerate(reserv.to_list()):
                    if reserved_by == ub_number:
                        reserved.append([i, reserv.room, j+1])
    return reserved
