from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Reservation

import helpers
import book.views as v


ubn = 1234

def index(request):
    if request.method == 'GET':
        #-------- GET UB# from request #--------
        # ubn = 1234
        #---------------------------------------
        reservations = helpers.get_reserved(ubn)
        rend_reserv = []
        for reserv in reservations:
            rend_reserv.append( [helpers.calc_day(reserv[0]).strftime('%A, %B %d %Y'),
                                v.ROOMS[reserv[1]], v.PERIODS[reserv[2]]])
        return render(request, 'revoke/revoke-index.html', {'reservations': rend_reserv})
    elif request.method == 'POST':
        #-------- GET UB# from request #--------
        # ubn = 1234
        #---------------------------------------
        if 'chosen' not in request.POST:
            return HttpResponseBadRequest('You did not choose anything')
        chosen = request.POST.getlist('chosen')
        reserved = helpers.get_reserved(ubn)
        for i in chosen:
            try:
                day, room, period = reserved[int(i)]
                Reservation.objects.filter( date=helpers.calc_day(day).isoformat(),
                                            room=room, period=period, ubnumber=int(ubn))[0].delete()
            except (ValueError, IndexError) as e:
                return HttpResponseBadRequest('Bad POST Request')
        return render(request, 'revoke/success.html', {'n': len(chosen)})
    else:
        return HttpResponseBadRequest('Bad Request')
