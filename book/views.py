from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest

import datetime

from .models import Reservation
import helpers


N_ROOMS = 3
DELTAS = ['0', '1']
MAX_RESERVATIONS = 2

PERIODS = [ '8:00 AM - 10:00 AM',
            '10:00 AM - 12:00 AM',
            '12:00 AM - 2:00 PM',
            '2:00 PM - 4:00 PM',
            '4:00 PM - 6:00 PM' ]

# resp.set_cookie('ubname', '7058034')

def index(request):
    if request.method == "GET":
        #-------- GET UB# from request #--------
        ubn = 1234
        #---------------------------------------
        delta = request.GET.get('day', -1)
        if delta not in DELTAS:
            return HttpResponseBadRequest("Bad GET Request")
        # calculate a date of requested day
        date = helpers.calc_day(int(delta))
        # get all rows from DB for requested date
        reservations = Reservation.objects.filter(date=date.isoformat())
        rooms = []
        # looping through all rooms
        for i in range(N_ROOMS):
            # get reservations for i-th room
            rooms.append(reservations.filter(room=i+1))
            # if room with booked timeslots
            if len(rooms[i]):
                # get list of timeslots with values
                rooms[i] = rooms[i][0].to_list()
            # all time slots are available
            else:
                rooms[i] = [0 for i in PERIODS]
        already_reserved = len(helpers.get_reserved(ubn))
        context = { 'date': date.strftime('%A, %B %d %Y'),
                    'day': delta,
                    'rooms_time': list(zip(PERIODS, *rooms)),
                    'already_reserved': already_reserved,
                    'available': MAX_RESERVATIONS - already_reserved, }
        return render(request, 'book/book-index.html', context)
    elif request.method == "POST":
        #-------- GET UB# from request #--------
        ubn = 1234
        #---------------------------------------
        print(request.POST)
        # handle empty POST request
        if 'room1' not in request.POST and 'room2' not in request.POST and 'room3' not in request.POST:
            return HttpResponseBadRequest('You did not choose any time frame')
        # parse POST equest and get list of chosen periods for every room
        rooms = [request.POST.getlist('room1'), request.POST.getlist('room2'), request.POST.getlist('room3')]
        delta = request.POST.get('day', -1)
        if (sum([len(i) for i in rooms]) + len(helpers.get_reserved(ubn))) > MAX_RESERVATIONS:
            return HttpResponseBadRequest('Oops... something bad happened. You try to reserve too much')
        if delta not in DELTAS:
            return HttpResponseBadRequest('Bad POST request')
        # get all reservations from DB for requested date
        date = helpers.calc_day(int(delta)).isoformat()
        reservations = Reservation.objects.filter(date=date)
        for i, room in enumerate(rooms):
            for period in room:
                refined = reservations.filter(room=i+1)
                # if record for requested room exists
                if refined.exists():
                    # try to reserve
                    if not refined[0].reserve(int(period), ubn):
                        return HttpResponseBadRequest('Already reserved')
                # create new record for a room
                else:
                    Reservation(date=date, room=i+1).reserve(int(period), ubn)
        return HttpResponse("Success!")
    else:
        return HttpResponseBadRequest("Bad Request")
