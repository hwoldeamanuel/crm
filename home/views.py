from django.shortcuts import render

# Create your views here.
from django.db.models import Max, Avg,Sum,Count
from django.db.models import Q

from program.models import Program, ImplementationArea
from portfolio.models import Portfolio
from django.contrib.auth.models import User
from report.models import IcnReport, ActivityReport
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
import json
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from program.models import Program
import json
from django.db.models import Max, Avg,Sum,Count

from collections import defaultdict
from itertools import chain
from django import template
from easyaudit.models import RequestEvent, CRUDEvent, LoginEvent
from conceptnote.models import Icn, Activity
from app_admin.models import Woreda
from fleet.models import *
import pandas as pd
from django.db.models.functions import TruncMonth

@login_required(login_url='login')
def home(request):
  total_program  =  Program.objects.count
  total_portfolio  =  Portfolio.objects.count
  total_user  =  User.objects.filter(is_active=True).count
  total_icn = Icn.objects.count
  total_activity = Activity.objects.count
  total_cn=0
  program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]
  program_cnbar = Program.objects.annotate(num_cn=Count("icn__activity",distinct=True) + Count("icn",distinct=True)).filter().order_by('-num_cn')[:12]
  program_cn = Program.objects.annotate(num_cn=Count("icn__activity",distinct=True) + Count("icn",distinct=True)).filter().order_by('-num_cn')[:11]
  for program in program_cn:
     total_cn = program.num_cn + total_cn

  total_woreda =  ImplementationArea.objects.values('woreda_id').distinct().count()
  icn_status =  Icn.objects.values('approval_status').annotate(icn_count=Count('id', distinct=True)).order_by('-icn_count')
  acn_status = Activity.objects.values('approval_status').annotate(acn_count=Count('id', distinct=True)).order_by('-acn_count')
  icn_report_status =  IcnReport.objects.values('approval_status').annotate(icn_count=Count('id', distinct=True))
  acn_report_status = ActivityReport.objects.values('approval_status').annotate(acn_count=Count('id', distinct=True))
  
  context = {'program_users':program_users, 'total_program': total_program,'total_cn':total_cn,'program_cnbar':program_cnbar,'program_cn':program_cn, 'total_portfolio':total_portfolio, 'total_user':total_user,  'total_woreda':total_woreda, 'total_icn':total_icn, 'total_activity':total_activity,'icn_status':icn_status, 'acn_status':acn_status, 'icn_report_status':icn_report_status, 'acn_report_status':acn_report_status}
  return render(request, 'home/dashboard_main.html', context)



@login_required(login_url='login')
def dashboard(request):
  total_program  =  Program.objects.count
  total_portfolio  =  Portfolio.objects.count
  total_user  =  User.objects.filter(is_active=True).count
  total_icn = Icn.objects.count
  total_cn=0
  total_activity = Activity.objects.count
  program_usersbar = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]
  program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:13]
  program_cn = Program.objects.annotate(num_cn=Count("icn__activity") + Count("icn")).filter(num_cn__gte=1).order_by('-num_cn')
  for program in program_cn:
     total_cn = program.num_cn + total_cn


  total_woreda =ImplementationArea.objects.values('woreda_id').distinct().count()
  icn_status =  Icn.objects.values('approval_status').annotate(icn_count=Count('id', distinct=True)).order_by('-icn_count')
  acn_status = Activity.objects.values('approval_status').annotate(acn_count=Count('id', distinct=True)).order_by('-acn_count')
  icn_report_status =  IcnReport.objects.values('approval_status').annotate(icn_count=Count('id', distinct=True))
  acn_report_status = ActivityReport.objects.values('approval_status').annotate(acn_count=Count('id', distinct=True))

  context = {'total_cn':total_cn,'program_cn':program_cn,'program_users':program_users ,'program_usersbar':program_usersbar, 'total_program': total_program, 'total_portfolio':total_portfolio, 'total_user':total_user,  'total_woreda':total_woreda, 'total_icn':total_icn, 'total_activity':total_activity, 'icn_status':icn_status, 'acn_status':acn_status, 'icn_report_status':icn_report_status, 'acn_report_status':acn_report_status}
  return render(request, 'home/dashboard2 copy.html', context)

@login_required(login_url='login')
def program_activity(request):
    
    program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]
    context = {'program_users':program_users }
    return render(request, 'home/program_activity.html', context)

def error_404(request, exception):
   
    return render(request, '404.html', status=404)
 
def error_500(request):
    return render(request, '505.html', status=500)

def get_date(request):
    if request.method == 'POST':
       month = request.POST.get("somedate")
       print(month)


@login_required(login_url='login')
def dashboard_fleet(request):
    total_field_office  =  FieldOffice.objects.count
    total_fleet =  Fleet.objects.values('tag_number').distinct().count()
    total_fleet_mc=  Fleet.objects.filter(ownership='Mercy Corps',vehicle_type='Vehicle').values('tag_number').distinct().count()
    total_fleet_mc_m =  Fleet.objects.filter(ownership='Mercy Corps',vehicle_type='MotorCycle').values('tag_number').distinct().count()
    total_fleet_r =  Fleet.objects.filter(ownership='Rental').values('tag_number').distinct().count()
    
    total_user  =  Generator.objects.count
    
    ff_gens = FieldOffice.objects.annotate(num_gen=Count('generator')).order_by('-num_gen')[:7]
    ff_fleet1 =  FieldOffice.objects.filter(assigned_to__ownership='Mercy Corps', assigned_to__vehicle_type ='Vehicle').annotate(num_vfleet=Count('assigned_to')).values('name','num_vfleet')
    ff_fleet2 = FieldOffice.objects.filter(assigned_to__ownership='Mercy Corps', assigned_to__vehicle_type ='MotorCycle').annotate(num_mfleet=Count('assigned_to')).values('name','num_mfleet')
    ffdf = pd.DataFrame.from_dict(ff_fleet1)
    ggdf = pd.DataFrame.from_dict(ff_fleet2)
    ff_fleet = ffdf.merge(ggdf,  how="outer", on="name", indicator=True)
    ff_fleet['num_vfleet'] = ff_fleet['num_vfleet'].fillna(0)
    
    ff_fleet['num_mfleet'] = ff_fleet['num_mfleet'].fillna(0)
    ff_fleet['num_mfleet'] = ff_fleet['num_mfleet'].astype(int)
    ff_fleet['total'] = ff_fleet['num_vfleet'] + ff_fleet['num_mfleet']   
    
    ff_fleet = ff_fleet.sort_values(by='total', ascending=False)
    
    

    ff_fleetr= FieldOffice.objects.filter(assigned_to__ownership ='Rental').annotate(num_fleet=Count('assigned_to')).order_by('-num_fleet')
    #program_cn = Program.objects.annotate(num_cn=Count("icn__activity",distinct=True) + Count("icn",distinct=True)).filter().order_by('-num_cn')[:12]
    ff_fleetmo= FieldOffice.objects.filter(assigned_to__vehicle_type ='MotorCycle').annotate(num_fleet=Count('assigned_to')).order_by('-num_fleet')
    x = Fleet_Log.objects.filter(log_start_date__gte='2023-07-01').annotate(created_at_month=TruncMonth('log_start_date')).values('created_at_month').annotate(km_driven=Sum('km_driven')).order_by('created_at_month')
    y = Fleet_Expense.objects.filter(expense_start_date__gte='2023-07-01').annotate(created_at_month=TruncMonth('expense_start_date')).values('created_at_month').annotate(total_expense=Sum('expense_value')).order_by('created_at_month')
    ydf = pd.DataFrame.from_dict(y)
    xdf = pd.DataFrame.from_dict(x)
    
    
    if not ydf.empty and not xdf.empty:
        all_request = xdf.merge(ydf, how='outer')
        all_request['km_driven'] = all_request['km_driven'].fillna(0)
        all_request['km_driven'] = all_request['km_driven'].astype(int)
        all_request['total_expense'] = all_request['total_expense'].fillna(0)
        all_request['total_expense'] = all_request['total_expense'].astype(int)

    elif ydf.empty and not xdf.empty:
        all_request = xdf
        all_request['km_driven'] = all_request['km_driven'].fillna(0)
        all_request['km_driven'] = all_request['km_driven'].astype(int)
    
    elif xdf.empty and not ydf.empty:
        all_request = ydf
        all_request['total_expense'] = all_request['total_expense'].fillna(0)
        all_request['total_expense'] = all_request['total_expense'].astype(int)


    elif ydf.empty and xdf.empty:
        all_request = pd.DataFrame(columns=['created_at_month', 'km_driven', 'total_expense'])

    ffs =  Log_Report.objects.filter(vehicle_type= 'Vehicle').annotate(created_at_month=TruncMonth('log_start_date')).values('created_at_month').annotate(day_total=Sum('day_total')).annotate(day_use=Sum('day_use')).annotate(day_available=Sum('day_available')).order_by('created_at_month')
    fdf = pd.DataFrame.from_dict(ffs)
    fdf['usage'] = fdf['day_use'] / fdf['day_total'] *100
    fdf['avalablity'] = fdf['day_available'] / fdf['day_total'] *100
    fdf['avalablity'] = fdf['avalablity'].astype(int)
    fdf['usage'] = fdf['usage'].astype(int)

    context = {'fdf': fdf, 'all_request': all_request,'total_field_office':total_field_office, 'total_fleet':total_fleet, 'total_fleet_mc':total_fleet_mc,
                'ff_fleetmo':ff_fleetmo,'ff_gens':ff_gens, 'ff_fleetr':ff_fleetr, 'total_fleet_r':total_fleet_r, 'total_user':total_user, 'ff_fleet':ff_fleet, 'total_fleet_mc_m':total_fleet_mc_m}
    
    return render(request, 'report/dashboard.html',context)