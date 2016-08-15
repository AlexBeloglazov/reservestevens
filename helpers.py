import datetime
from book.models import Reservation
from django.db.models import Q

MAX_DAYS = 2

# returns date object that represents requested day. d is a delta (difference between today and requested date in days)
# d=0 - today, d=1 - next day
def calc_day(d):
    # latest hour to reserve a room for today
    MAX_HOUR = 16
    today = datetime.date.today()
    # if today is monday, tuesday, wednesday or thursday and before 4PM
    if today.weekday() < 4 and datetime.datetime.now().hour >= MAX_HOUR:
        # increase delta by 1 since it is too late
        d = d + 1
    # if today is friday
    if today.weekday() == 4:
        # if it is before 4PM then still can reserve for today and next availbale day will be monday.
        # if it is after 4PM then first reservation day is monday and next is tuesday
        d = (d + d*2) if datetime.datetime.now().hour < MAX_HOUR else (d + 3)
    # handling weekends
    # if saturday
    elif today.weekday() == 5:
        d = d + 2
    # if sunday
    elif today.weekday() == 6:
        d = d + 1
    return today + datetime.timedelta(days=d)

# returns list of reservations in form [[day[0,1], room[0,1,2], period[0,1,2,3]], ...] for given UB#
def get_reserved(ub_number):
    reserved = []
    # loop through days (0-today, 1-next day)
    for i in range(MAX_DAYS):
        # get all reservations for i-th day
        day = Reservation.objects.filter(date=calc_day(i).isoformat(), ubnumber=ub_number)
        # loop through reservations
        for reserv in day:
            r = [i]
            # extending list 'r' with room index and reservation period index
            r.extend(reserv.to_list())
            # append [day, room, period] to reserved
            reserved.append(r)
    return reserved
