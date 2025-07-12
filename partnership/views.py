from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
import json
from django.db.models import Count
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .models import Partnership


def convertmonth(created):
    #template = '%(function)s(MONTH from %(expressions)s)'
    #output_field = models.IntegerField()fdfd
    return created.strftime("%m-%Y")

@login_required(login_url='login')
def partnership(request):
    partnerships = Partnership.objects.all()
    context = {'partnerships': partnerships}
    return render(request, 'partnership.html', context)

@login_required(login_url='login')
def partnership_profile(request, id):
    partnership = Partnership.objects.get(id = id)
    context = {'partnership': partnership}
    return render(request, 'partnership_profile.html', context)