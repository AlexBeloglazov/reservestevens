from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import datetime

from .models import Reservation
import helpers


MAX_RESERVATIONS = 2
DELTAS = ['0', '1']
ROOMS = ['Room #0', 'Room #1', 'Room #2']
PERIODS = [ '8:30 AM - 10:30 AM',
            '10:30 AM - 12:30 AM',
            '12:30 AM - 2:30 PM',
            '2:30 PM - 4:30 PM',]

@login_required
def index(request, delta):
    if request.method == "GET":
        # get ubnumber of user
        ubn = request.user.ubstudent.ubnumber
        # calculate a date of requested day
        date = helpers.calc_day(int(delta))
        # get all reservations from DB for requested date
        reservations = Reservation.objects.filter(date=date.isoformat())
        # rooms will be a list containing three lists, one for each room
        rooms = []
        # looping through all rooms
        for i in range(len(ROOMS)):
            # appending list for i-th room
            rooms.append([])
            # looping through all periods possible for room
            for period in range(len(PERIODS)):
                # appending either True or False based on period availability
                rooms[i].append(reservations.filter(room=i, period=period).exists())
        # number of reservations for logged user
        already_reserved = len(helpers.get_reserved(ubn))
        context = { 'date': date.strftime('%A, %B %d %Y'),
                    'day': delta,
                    'rooms_time': list(zip(PERIODS, *rooms)),
                    'rooms': ROOMS,
                    'already_reserved': already_reserved,
                    'available': MAX_RESERVATIONS - already_reserved, }
        return render(request, 'book/book-index.html', context)
    elif request.method == "POST":
        # get ubnumber of user
        ubn = request.user.ubstudent.ubnumber
        # just in case handle empty POST request
        if 'room0' not in request.POST and 'room1' not in request.POST and 'room2' not in request.POST:
            return HttpResponseBadRequest('You did not choose any time frame')
        # parse POST request and get list of chosen periods for every room
        rooms = [request.POST.getlist('room0'), request.POST.getlist('room1'), request.POST.getlist('room2')]
        if (sum([len(i) for i in rooms]) + len(helpers.get_reserved(ubn))) > MAX_RESERVATIONS:
            return HttpResponseBadRequest('Oops... something bad happened. You try to reserve too much')
        if delta not in DELTAS:
            return HttpResponseBadRequest('Bad POST request')
        date = helpers.calc_day(int(delta))
        # get all reservations from DB for requested date
        reservations = Reservation.objects.filter(date=date.isoformat())
        # list will contain all reservations made. Will be used in template
        r_render = []
        try:
            for i, room in enumerate(rooms):
                for period in room:
                    # collect info for renderer
                    r_render.append([ROOMS[i], PERIODS[int(period)]])
                    # one last check to make sure everything goes smoothly
                    if reservations.filter(room=i, period=int(period)).exists():
                        return HttpResponseBadRequest('Already reserved')
                    # create new reservation for a room
                    else:
                        request.user.ubstudent.reservation_set.create(date=date.isoformat(), room=i, period=period)
        except ValueError:
            return HttpResponseBadRequest('Bad POST request')
        return render(request, 'book/success.html', {'date': date.strftime('%A, %B %d %Y'), 'reserved': r_render})
    else:
        return HttpResponseBadRequest("Bad Request")
