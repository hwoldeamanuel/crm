from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
import json
from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import QueryDict
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from portfolio.models import Portfolio
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from collections import namedtuple
from .forms import PortfolioForm, FieldOfficeForm
from .models import Portfolio, FieldOffice
from easyaudit.models import LoginEvent, RequestEvent, CRUDEvent
from collections import defaultdict
from collections import defaultdict
from itertools import chain
from django.db.models import F
from conceptnote.models import Icn, Activity
from django.db import models
from django.db.models import Func
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Q
from collections import defaultdict
from django.contrib.auth.decorators import permission_required
import pandas as pd
from partnership.models import Partnership

def convertmonth(created):
    #template = '%(function)s(MONTH from %(expressions)s)'
    #output_field = models.IntegerField()
    return created.strftime("%m-%Y")

@login_required(login_url='login')
def portfolios(request):
    partnership = Partnership.objects.all()
    portfolios = Portfolio.objects.filter().exclude(id=1).order_by('id')
    context = {'portfolios': portfolios}
    return render(request, 'portfolios.html', context)


@login_required(login_url='login')
def mercycorps(request):
    portfolio = Portfolio.objects.filter(id=1)
   
    x = Icn.objects.filter(Q(ilead_agency__in=portfolio) | Q(ilead_co_agency__in=portfolio)).annotate(created_at_month=TruncMonth('created')).values('created_at_month').annotate(icn_count=Count('id')).order_by('created_at_month')
    y = Activity.objects.filter(Q(alead_agency__in=portfolio) | Q(alead_co_agency__in=portfolio)).annotate(created_at_month=TruncMonth('created')).values('created_at_month').annotate(acn_count=Count('id')).order_by('created_at_month')
  
    #pia = ImplementationArea.objects.filter(program__in=program).values_list('region').distinct('region')
    
    #print(pia
    ydf = pd.DataFrame.from_dict(y)
    xdf = pd.DataFrame.from_dict(x)
    if not ydf.empty and not xdf.empty:
        all_request = xdf.merge(ydf, how='outer')
        all_request['acn_count'] = all_request['acn_count'].fillna(0)
        all_request['acn_count'] = all_request['acn_count'].astype(int)
        all_request['icn_count'] = all_request['icn_count'].fillna(0)
        all_request['icn_count'] = all_request['icn_count'].astype(int)

    elif ydf.empty and not xdf.empty:
        all_request = xdf
        all_request['icn_count'] = all_request['icn_count'].fillna(0)
        all_request['icn_count'] = all_request['icn_count'].astype(int)

    elif ydf.empty and xdf.empty:
        all_request = pd.DataFrame(columns=['created_at_month', 'icn_count', 'acn_count'])

    #all_request =  Icn.objects.filter(Q(ilead_agency__in=portfolio) | Q(ilead_co_agency__in=portfolio)).annotate(m=TruncMonth('created')).values("m").annotate(icn_count=Count('id', distinct=True)).annotate(activity_count=Count('activity', distinct=True))
    
    portfolio = Portfolio.objects.get(id=1)
    total_icn  =  Icn.objects.filter(Q(ilead_agency=portfolio.id) | Q(ilead_co_agency=portfolio.id)).count
    total_acn  =  Activity.objects.filter(Q(alead_agency=portfolio.id) | Q(alead_co_agency=portfolio.id)).count
    
    total_program = Icn.objects.filter(Q(ilead_agency=portfolio.id) | Q(ilead_co_agency=portfolio.id)).values('program__title').distinct().count()
    context = {'portfolio': portfolio, 'all_request':all_request,'total_icn':total_icn, 'total_acn':total_acn, 'total_program':total_program}
    return render(request, 'partial/portfolio_mercycorps.html', context)





@login_required(login_url='login')
def portfolios_list(request):
    partnership = Partnership.objects.all()
    portfolios = Portfolio.objects.filter(category__name="Other").exclude(id=1).order_by('id')
 
    context = {'portfolios': portfolios}
    return render(request, 'partial/portfolios_list.html', context)




@login_required(login_url='login')
@permission_required("portfolio.can_change_portfolio", raise_exception=True)
def edit_portfolio(request, id):
    portfolio = get_object_or_404(Portfolio, id=id)
    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            instance =form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "PortfolioListChanged": None,
                        "showMessage": f"{instance.title} updated."
                    })
                }
            )
    else:
        form = PortfolioForm(instance=portfolio)
    return render(request, 'partial/portfolio_form.html', {
        'form': form,
        'portfolio': portfolio,
    })

@login_required(login_url='login')
@permission_required("portfolio.can_add_portfolio", raise_exception=True)
def add_porfolio(request):
    
    form = PortfolioForm()
    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            
            instance = form.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "PortfolioListChanged": None,
                         "showMessage": f"{instance.title} updated."

                        
                    })
                }
            )
    else:
        form = PortfolioForm()
    return render(request, 'partial/portfolio_form.html', {
        'form': form,
    })

@login_required(login_url='login')
@permission_required("portfolio.can_delete_portfolio", raise_exception=True)
def delete_portfolio(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    portfolio.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "PortfolioListChanged": None,
                "showMessage": f"{portfolio.title} deleted."
            })
        })

@login_required(login_url='login')
def portfolio_filter(request):
    partnership = Partnership.objects.all()
    query = request.GET.get('search', '')
    
    
    
    if query:
        qs1 = Portfolio.objects.filter(title__icontains=query).exclude(id=1)
        qs2 = Portfolio.objects.distinct().filter(type__name__icontains=query).exclude(id=1)
        qs3 = Portfolio.objects.distinct().filter(category__name__icontains=query).exclude(id=1)
        
        portfolios = qs1.union(qs2, qs3).order_by('id')
       
        
    else:
        portfolios = Portfolio.objects.filter(id__in=partnership.values('portfolio_id')).exclude(id=1).order_by('id')

    context = {'portfolios': portfolios}
    return render(request, 'partial/portfolios_list.html', context)

def categories(request):
    form = PortfolioForm(request.GET)
    return HttpResponse(form['category'])

@login_required(login_url='login')
def portfolio_detail(request, pk):
    portfolio = Portfolio.objects.filter(id=pk)
    x = Icn.objects.filter(Q(ilead_agency__in=portfolio) | Q(ilead_co_agency__in=portfolio)).annotate(created_at_month=TruncMonth('created')).values('created_at_month').annotate(icn_count=Count('id')).order_by('created_at_month')
    y = Activity.objects.filter(Q(alead_agency__in=portfolio) | Q(alead_co_agency__in=portfolio)).annotate(created_at_month=TruncMonth('created')).values('created_at_month').annotate(acn_count=Count('id')).order_by('created_at_month')
  
    #pia = ImplementationArea.objects.filter(program__in=program).values_list('region').distinct('region')
    
    #print(pia
    ydf = pd.DataFrame.from_dict(y)
    xdf = pd.DataFrame.from_dict(x)
    if not ydf.empty and not xdf.empty:
        all_request = xdf.merge(ydf, how='outer')
        all_request['acn_count'] = all_request['acn_count'].fillna(0)
        all_request['acn_count'] = all_request['acn_count'].astype(int)
        all_request['icn_count'] = all_request['icn_count'].fillna(0)
        all_request['icn_count'] = all_request['icn_count'].astype(int)

    elif ydf.empty and not xdf.empty:
        all_request = xdf
        all_request['icn_count'] = all_request['icn_count'].fillna(0)
        all_request['icn_count'] = all_request['icn_count'].astype(int)

    elif ydf.empty and xdf.empty:
        all_request = pd.DataFrame(columns=['created_at_month', 'icn_count', 'acn_count'])
        
    
        

    portfolio = Portfolio.objects.get(id=pk)
    total_icn  =  Icn.objects.filter(Q(ilead_agency=portfolio.id) | Q(ilead_co_agency=portfolio.id)).count
    total_acn  =  Activity.objects.filter(Q(alead_agency=portfolio.id) | Q(alead_co_agency=portfolio.id)).count
    
    total_program = Partnership.objects.filter(portfolio_id=portfolio.id).values('program_id').distinct().count()
    context = {'portfolio': portfolio, 'all_request':all_request,'total_icn':total_icn, 'total_acn':total_acn, 'total_program':total_program}
    return render(request, 'portfolio.html', context)

def pregion(request, id):
    portfolio = get_object_or_404(Portfolio, pk=id)
    if request.method == "POST":
        form = FieldOfficeForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.portfolio = Portfolio.objects.get(pk=id)
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FieldOfficeListChanged": None,
                        "showMessage": f"{instance.woreda} added."
                    })
                })
    
    form = FieldOfficeForm()
    context = {'form': form}
    
    return render(request, 'partial/portfolio_area_form.html', context)

@login_required(login_url='login')
def pzones(request):
    form = FieldOfficeForm(request.GET)
    return HttpResponse(form['zone'])


   
@login_required(login_url='login')
def pworedas(request):
    form = FieldOfficeForm(request.GET)
    return HttpResponse(form['woreda'])

@login_required(login_url='login')
def fieldoffices(request, id):
    return render(request, 'partial/portfolio_fieldoffice.html', {
        'fieldoffices': FieldOffice.objects.filter(portfolio_id=id),
    })

@login_required(login_url='login')
def portfolio_profile(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    context = {'portfolio': portfolio}
    return render(request, 'partial/portfolio_profile.html', context)

@login_required(login_url='login')
@permission_required("portfolio.can_change_fieldoffice", raise_exception=True)
def fieldoffice_edit(request, pk):
    fieldoffice = get_object_or_404(FieldOffice, pk=pk)
    if request.method == "POST":
        form = FieldOfficeForm(request.POST, instance=fieldoffice)
        if form.is_valid():
            instance = form.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FieldOfficeListChanged": None,
                        "showMessage": f"{instance.woreda} added."
                    })
                })
    
    form = FieldOfficeForm(instance=fieldoffice)
    context = {'form': form, 'fieldoffice':fieldoffice}
    
    return render(request, 'partial/portfolio_area_form.html', context)

@login_required(login_url='login')
@permission_required("portfolio.can_delete_fieldoffice", raise_exception=True)
def remove_fieldoffice(request, pk):
    fieldoffice = get_object_or_404(FieldOffice, pk=pk)
    fieldoffice.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "FieldOfficeListChanged": None,
                "showMessage": f"{fieldoffice.woreda} deleted."
            })
        })


@login_required(login_url='login')
def portfolio_conceptnotes(request, id):
    
    portfolio = Portfolio.objects.filter(id=id)
    qsi = Icn.objects.filter(Q(ilead_agency__in=portfolio) | Q(ilead_co_agency__in=portfolio)).only("title", "id","user","program_lead","technical_lead","finance_lead","status","approval_status","created","final_report_due_date","icnreport__approval_status").annotate(report = F('icnreport__approval_status'))
    qsa = Activity.objects.filter(Q(alead_agency__in=portfolio) | Q(alead_co_agency__in=portfolio)).only("title", "id", "user","program_lead","technical_lead","finance_lead","status","approval_status","created","final_report_due_date", "activityreport__approval_status").annotate(report = F('activityreport__approval_status'))
      
       
    conceptnotes = sorted(list(chain(qsi, qsa)), key=lambda instance: instance.created, reverse=True)
    
    context = {'conceptnotes': conceptnotes}

    return render(request, 'partial/portfolio_conceptnotes.html', context)

@login_required(login_url='login')
def portfolio_partnerships(request, id): 
    partnerships = Partnership.objects.filter(portfolio_id=id)
    context = {'partnerships': partnerships}
    return render(request, 'partial/portfolio_partnership.html', context)