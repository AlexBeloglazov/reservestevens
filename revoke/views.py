from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import Reservation

import helpers
import book.views as v

@login_required
def index(request):
    ubn = request.user.ubstudent.ubnumber
    # cancelling chosen reservations
    if request.method == 'POST':
        if 'chosen' not in request.POST:
            return HttpResponseBadRequest('You did not choose anything')
        chosen = request.POST.getlist('chosen')
        reserved = helpers.get_reserved(ubn)
        for i in chosen:
            try:
                day, room, period = reserved[int(i)]
                Reservation.objects.filter( date=helpers.calc_day(day).isoformat(),
                                            room=room, period=period, ubnumber=ubn)[0].delete()
            except (ValueError, IndexError) as e:
                return HttpResponseBadRequest('Bad POST Request')
    # get all reservations for student with ub# ubn
    reservations = helpers.get_reserved(ubn)
    rend_reserv = []
    for reserv in reservations:
        rend_reserv.append( [helpers.calc_day(reserv[0]).strftime('%A, %B %d %Y'),
                            v.ROOMS[reserv[1]], v.PERIODS[reserv[2]]])
    if request.method == 'GET':
        return render(request, 'revoke/revoke-index.html', {'reservations': rend_reserv})
    elif request.method == 'POST':
        return render(request, 'revoke/revoke-index.html', {'reservations': rend_reserv, 'n': len(chosen)})
    else:
        return HttpResponseBadRequest('Bad Request')
