from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest

import datetime

from .models import Reservation
import helpers


MAX_RESERVATIONS = 2
DELTAS = ['0', '1']
ROOMS = ['Room #0', 'Room #1', 'Room #2']
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
        for i in range(len(ROOMS)):
            rooms.append([])
            for period in range(len(PERIODS)):
                rooms[i].append(reservations.filter(room=i, period=period).exists())
        already_reserved = len(helpers.get_reserved(ubn))
        context = { 'date': date.strftime('%A, %B %d %Y'),
                    'day': delta,
                    'rooms_time': list(zip(PERIODS, *rooms)),
                    'rooms': ROOMS,
                    'already_reserved': already_reserved,
                    'available': MAX_RESERVATIONS - already_reserved, }
        return render(request, 'book/book-index.html', context)
    elif request.method == "POST":
        #-------- GET UB# from request #--------
        ubn = 1234
        #---------------------------------------
        # print(request.POST)
        # just in case handle empty POST request
        if 'room0' not in request.POST and 'room1' not in request.POST and 'room2' not in request.POST:
            return HttpResponseBadRequest('You did not choose any time frame')
        # parse POST request and get list of chosen periods for every room
        rooms = [request.POST.getlist('room0'), request.POST.getlist('room1'), request.POST.getlist('room2')]
        delta = request.POST.get('day', -1)
        if (sum([len(i) for i in rooms]) + len(helpers.get_reserved(ubn))) > MAX_RESERVATIONS:
            return HttpResponseBadRequest('Oops... something bad happened. You try to reserve too much')
        if delta not in DELTAS:
            return HttpResponseBadRequest('Bad POST request')
        date = helpers.calc_day(int(delta))
        # get all reservations from DB for requested date
        reservations = Reservation.objects.filter(date=date.isoformat())
        r_render = []
        try:
            for i, room in enumerate(rooms):
                for period in room:
                    # collect info for renderer
                    r_render.append([ROOMS[i], PERIODS[int(period)]])
                    # one last check to make sure everything goes smoothly
                    if reservations.filter(room=i, period=int(period)).exists():
                        return HttpResponseBadRequest('Already reserved')
                    # create new record for a room
                    else:
                        Reservation(date=date.isoformat(), room=i, period=period, ubnumber=ubn).save()
        except ValueError:
            return HttpResponseBadRequest('Bad POST request')
        print(r_render)
        return render(request, 'book/success.html', {'date': date.strftime('%A, %B %d %Y'), 'reserved': r_render})
    else:
        return HttpResponseBadRequest("Bad Request")
