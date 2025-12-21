from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.db.models.functions import TruncMonth
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
# Create your views here.
from django.contrib.auth.decorators import login_required

from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
import json
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

import json
from django.db.models import Max, Avg,Sum,Count
from django.db.models import Q
from collections import defaultdict
from itertools import chain
from django import template
import requests
import pandas as pd
from django.core import serializers
from datetime import datetime

from fleet.models import Fleet, Fleet_Log, Fleet_Expense, Generator, Generator_Report, Missing_Log, Missing_Expense, Log_Report, Missed_Expense, Expense_Report
from fleet.forms import FleetForm, FleetLogForm, FleetLogFormEdit, FleetExpenseFormEdit, FleetExpenseForm, GeneratorForm, GeneratorReportForm, GeneratorReportFormEdit
from .forms import MissingLogForm

from datetime import datetime, timedelta
from django.utils import timezone
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from .models import Fleet
from fleet.models import  Fleet, Fleet_Expense, Generator, Generator_Report, Fleet_Log, Missing_Log, Missing_Expense
from fleet.forms import FleetForm, FleetLogForm, FleetLogFormEdit, FleetExpenseFormEdit, FleetExpenseForm, GeneratorForm, GeneratorReportForm, GeneratorReportFormEdit
from app_admin.models import FieldOffice



@login_required(login_url='login')
def fleets(request):
    user = request.user
    if user.is_superuser:
        fleets = Fleet.objects.all().order_by('field_office','id')
    else:
        
        fleets = Fleet.objects.filter(field_office=user.profile.field_office).order_by('field_office','id')
    
    context = {'fleets':fleets }
    
    return render(request, 'fleet/fleets.html', context)


@login_required(login_url='login')
def fleet(request, id):
    fleet = get_object_or_404(Fleet,id=id)
    fleet_log = Fleet_Log.objects.filter(fleet=fleet).order_by('log_start_date')
    fleet_expense = Fleet_Expense.objects.filter(fleet=fleet).order_by('expense_start_date')
    fleet = Fleet.objects.get(id=id)
    x = Fleet_Log.objects.filter(fleet=fleet).annotate(created_at_month=TruncMonth('log_start_date')).values('created_at_month').annotate(km_driven=Sum('km_driven')).order_by('created_at_month')
    y = Fleet_Expense.objects.filter(fleet=fleet).annotate(created_at_month=TruncMonth('expense_start_date')).values('created_at_month').annotate(total_expense=Sum('expense_value')).order_by('created_at_month')
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
        
        all_request['km_driven'] = all_request['km_driven'].astype(int)
        all_request['km_driven'] = all_request['km_driven'].fillna(0)
    
    elif xdf.empty and not ydf.empty:
        all_request = ydf
        all_request['total_expense'] = all_request['total_expense'].fillna(0)
        all_request['total_expense'] = all_request['total_expense'].astype(int)


    elif ydf.empty and xdf.empty:
        all_request = pd.DataFrame(columns=['created_at_month', 'km_driven', 'total_expense'])

    all_request = all_request.sort_values(['created_at_month'],ascending = False).head(12)
    all_request = all_request.sort_values(['created_at_month'],ascending = True)
    context = {'all_request': all_request }
    
    context = {'fleet':fleet, 'fleet_log':fleet_log, 'fleet_expense':fleet_expense, 'all_request': all_request }
    
    return render(request, 'fleet/fleet.html', context)

@login_required(login_url='login')
def fleet_profile(request, id):
    fleet = get_object_or_404(Fleet,id=id)
    
    
    context = {'fleet':fleet,  }
    
    return render(request, 'fleet/partial/fleet_profile.html', context)


@login_required(login_url='login')
def fleet_list(request):
   
    user = request.user
    if user.is_superuser:
        fleets = Fleet.objects.all().order_by('field_office','id')
    else:
        
        fleets = Fleet.objects.filter(field_office=user.profile.field_office).order_by('field_office','id')
    context = {'fleets':fleets, }
    
    return render(request, 'fleet/partial/fleets_list.html', context)


@login_required(login_url='login')
def edit_fleet(request, id):
    fleet = Fleet.objects.get(pk=id)
    if request.method == "POST":
        form = FleetForm(request.POST, request.FILES, instance=fleet)
        if form.is_valid():
            instance =form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FleetProfileChanged": None,
                        "showMessage": f"{instance.id} updated."
                    })
                }
            )
        else:
            form = FleetForm(instance=fleet)
            return render(request, 'fleet/partial/fleet_form.html', {
             'form': form,    'fleet': fleet,
            })

    else:
        form = FleetForm(instance=fleet)
    return render(request, 'fleet/partial/fleet_form.html', {
        'form': form,
        'fleet': fleet,
    })


@login_required(login_url='login')
def edit_fleet_log(request, fid, id):
    fleet = Fleet.objects.get(id=fid)
    fleet_log = Fleet_Log.objects.get(pk=id)
    if request.method == "POST":
        form = FleetLogFormEdit(request.POST, request.FILES, instance=fleet_log)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.tag_number = fleet.tag_number
            instance.field_office = fleet.field_office
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FleetListChanged": None,
                        "showMessage": f"{instance.id} updated."
                    })
                }
            )
    
    
        form = FleetLogFormEdit(request.POST, instance=fleet_log, fleet=fleet.id)
        return render(request, 'fleet/partial/fleetlog_form.html', {
        'form': form,
        'fleet_log': fleet_log,
        })
    
    form = FleetLogFormEdit(instance=fleet_log, fleet=fleet.id)
    return render(request, 'fleet/partial/fleetlog_form.html', {
        'form': form,
        'fleet_log': fleet_log,
        })

@login_required(login_url='login')
def add_fleet(request):
    
    form = FleetForm()
    if request.method == "POST":
        form = FleetForm(request.POST, request.FILES)
        if form.is_valid():
            
            instance = form.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FleetListChanged": None,
                         "showMessage": f"{instance.tag_number} updated."

                        
                    })
                }
            )
    else:
        form = FleetForm()
    return render(request, 'fleet/partial/fleet_form.html', {
        'form': form,
    })

@login_required(login_url='login')
def add_fleet_log(request, id):
    fleet = Fleet.objects.get(id=id)
    form = FleetLogForm(fleet = fleet.id)
    if request.method == "POST":
        form = FleetLogForm(request.POST, request.FILES)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.tag_number = fleet.tag_number
            instance.field_office = fleet.field_office
            instance.save()
                        
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FleetListChanged": None,
                         "showMessage": f"{instance.tag_number} updated."

                        
                    })
                }
            )
        form = FleetLogForm(request.POST,request.FILES, fleet=fleet.id)   
       
        context = {'form':form}
        return render(request, 'fleet/partial/fleetlog_form.html', context)
    
    form = FleetLogForm(fleet = fleet.id)
    
    context = {'fleet': fleet, 'form':form }
    return render(request, 'fleet/partial/fleetlog_form.html', context)



@login_required(login_url='login')
def fieldoffice(request):
    return render(request, 'user/fieldoffice.html')


@login_required(login_url='login')
def fleet_filter(request):
    user = request.user
    if user.is_superuser:
        all_fleets = Fleet.objects.all().order_by('field_office','id')
    else:
        
        all_fleets = Fleet.objects.filter(field_office=user.profile.field_office).order_by('field_office','id')
    
    query = request.GET.get('search', '')
    
    
    
    if query:
        qs1 = all_fleets.filter(tag_number__icontains=query)
        qs2 = all_fleets.filter(field_office__name__icontains=query)
        qs3 = all_fleets.filter(ownership__icontains=query)
        qs4 = all_fleets.filter(vehicle_type__icontains=query)
        
        fleets = qs1.union(qs2, qs3, qs4).order_by('field_office','id')
       
        
    else:
        fleets = all_fleets

    context = {'fleets': fleets}
    return render(request, 'fleet/partial/fleets_list.html', context)

@login_required(login_url='login')
def download_logsheet(request, id):
    log_sheet = get_object_or_404(Fleet_Log, id=id)
    response = HttpResponse(log_sheet.log_sheet, content_type='application/docx')
    response['Content-Disposition'] = f'attachment; filename="{log_sheet.log_sheet}"'
    return response


@login_required(login_url='login')
def partial_fleet_log(request, id):
    fleet = Fleet.objects.get(id=id)
    fleet_log = Fleet_Log.objects.filter(fleet=fleet).order_by('log_start_date')
    context = {'fleet_log':fleet_log, }
    
    return render(request, 'fleet/partial/partial_fleet_log.html', context)

@login_required(login_url='login')
def remove_fleetlog(request, pk):
    fleetlog = get_object_or_404(Fleet_Log, pk=pk)
    fleetlog.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "FleetListChanged": None,
                "showMessage": f"{fleetlog.id} deleted."
            })
        })


@login_required(login_url='login')
def fleet_expenses(request):
   
    fleet_expenses = Fleet_Expense.objects.all().order_by('field_office','id')
    context = {'fleet_expenses':fleet_expenses, }
    
    return render(request, 'fleet/partial/fleets_list.html', context)

@login_required(login_url='login')
def edit_fleet_expense(request, fid, id):
    fleet = Fleet.objects.get(id=fid)
    fleet_expense = Fleet_Expense.objects.get(pk=id)
    if request.method == "POST":
        form = FleetExpenseFormEdit(request.POST, request.FILES, instance=fleet_expense)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.tag_number = fleet.tag_number
            instance.field_office = fleet.field_office
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FleetListChanged": None,
                        "showMessage": f"{instance.id} updated."
                    })
                }
            )
    
    
        form = FleetExpenseFormEdit(request.POST, instance=fleet_expense, fleet=fleet.id)
        return render(request, 'fleet/partial/fleetexpense_form.html', {
        'form': form,
        'fleet_expense': fleet_expense,
        })
    
    form = FleetExpenseFormEdit(instance=fleet_expense, fleet=fleet.id)
    return render(request, 'fleet/partial/fleetexpense_form.html', {
        'form': form,
        'fleet_expense': fleet_expense,
        })


@login_required(login_url='login')
def partial_fleet_expense(request, id):
    fleet = Fleet.objects.get(id=id)
    fleet_expense= Fleet_Expense.objects.filter(fleet=fleet).order_by('expense_start_date')
    context = {'fleet_expense':fleet_expense, }
    
    return render(request, 'fleet/partial/partial_fleet_expense.html', context)


@login_required(login_url='login')
def remove_fleetexpense(request, pk):
    fleetexpense = get_object_or_404(Fleet_Expense, pk=pk)
    fleetexpense.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "FleetListChanged": None,
                "showMessage": f"{fleetexpense.id} deleted."
            })
        })


@login_required(login_url='login')
def add_fleet_expense(request, id):
    fleet = Fleet.objects.get(id=id)
    form = FleetExpenseForm(fleet = fleet.id)
    if request.method == "POST":
        form = FleetExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.tag_number = fleet.tag_number
            instance.field_office = fleet.field_office
            instance.save()
                        
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FleetListChanged": None,
                         "showMessage": f"{instance.id} updated."

                        
                    })
                }
            )
        form = FleetExpenseForm(request.POST,request.FILES, fleet=fleet.id)   
       
        context = {'fleet': fleet, 'form':form }
        return render(request, 'fleet/partial/fleetexpense_form.html', context)
    
    form = FleetExpenseForm(fleet = fleet.id)
    
    context = {'fleet': fleet, 'form':form }
    return render(request, 'fleet/partial/fleetexpense_form.html', context)


@login_required(login_url='login')
def fleet_activity(request, id):
   
    fleet = get_object_or_404(Fleet,id=id)
    x = Fleet_Log.objects.filter(fleet=fleet).annotate(created_at_month=TruncMonth('log_start_date')).values('created_at_month').annotate(km_driven=Sum('km_driven')).order_by('created_at_month')
    y = Fleet_Expense.objects.filter(fleet=fleet).annotate(created_at_month=TruncMonth('expense_start_date')).values('created_at_month').annotate(total_expense=Sum('expense_value')).order_by('created_at_month')
    ydf = pd.DataFrame.from_dict(y)
    xdf = pd.DataFrame.from_dict(x)

    
    if not ydf.empty and not xdf.empty:
        all_request = xdf.merge(ydf, how='outer')
        all_request['km_driven'] = all_request['km_driven'].fillna(0)
        all_request['km_driven'] = all_request['km_driven'].astype(float)
        all_request['total_expense'] = all_request['total_expense'].fillna(0)
        all_request['total_expense'] = all_request['total_expense'].astype(float)

    elif ydf.empty and not xdf.empty:
        all_request = xdf
        
        all_request['km_driven'] = all_request['km_driven'].astype(float)
        all_request['km_driven'] = all_request['km_driven'].fillna(0)
    
    elif xdf.empty and not ydf.empty:
        all_request = ydf
        all_request['total_expense'] = all_request['total_expense'].fillna(0)
        all_request['total_expense'] = all_request['total_expense'].astype(float)


    elif ydf.empty and xdf.empty:
        all_request = pd.DataFrame(columns=['created_at_month', 'km_driven', 'total_expense'])


    all_request = all_request.sort_values(['created_at_month'],ascending = False).head(12)
    all_request = all_request.sort_values(['created_at_month'],ascending = True)
    context = {'all_request': all_request }
    return render(request, 'fleet/partial/fleet_activity.html', context)


@login_required(login_url='login')
def generators(request):
    user = request.user
    if user.is_superuser:
        generators = Generator.objects.all().order_by('field_office','id')
    else:
        
        generators = Generator.objects.filter(field_office=user.profile.field_office).order_by('field_office','id')
    
    context = {'generators':generators }
    
    return render(request, 'generator/generators.html', context)


@login_required(login_url='login')
def generator(request, id):
    generator = Generator.objects.get(id=id)
    generator_report = Generator_Report.objects.filter(generator=generator).order_by('report_start_date')
    all_request = Generator_Report.objects.filter(generator=generator).annotate(created_at_month=TruncMonth('report_start_date')).values('created_at_month').annotate(ops_hr=Sum('operated_time_hr')).annotate(cost_br=Sum('fuel_cost_br')).order_by('created_at_month')
   
    context = {'generator':generator, 'generator_report': generator_report, 'all_request':all_request }
    
    return render(request, 'generator/generator.html', context)


@login_required(login_url='login')
def generator_activity(request, id):
    gen = Generator.objects.get(id=id)
    all_request = Generator_Report.objects.filter(generator=gen).annotate(created_at_month=TruncMonth('report_start_date')).values('created_at_month').annotate(ops_hr=Sum('operated_time_hr')).annotate(cost_br=Sum('fuel_cost_br')).order_by('created_at_month')
    context = {'all_request':all_request }
    return render(request, 'generator/partial/generator_activity.html', context)


@login_required(login_url='login')
def edit_generator(request, id):
    generator = Generator.objects.get(pk=id)
    if request.method == "POST":
        form = GeneratorForm(request.POST, request.FILES, instance=generator)
        if form.is_valid():
            instance =form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "GeneratorChanged": None,
                        "showMessage": f"{instance.id} updated."
                    })
                }
            )
        else:
            form = GeneratorForm(instance=generator)
            return render(request, 'generator/partial/generator_form.html', {
             'form': form,    'generator': generator,
            })

    else:
        form = GeneratorForm(instance=generator)
    return render(request, 'generator/partial/generator_form.html', {
        'form': form,
        'generator': generator,
    })

@login_required(login_url='login')
def edit_generator_report(request, fid, id):
    generator = Generator.objects.get(id=fid)
    generator_report = Generator_Report.objects.get(pk=id)
    if request.method == "POST":
        form = GeneratorReportFormEdit(request.POST, request.FILES, instance=generator_report)
        if form.is_valid():
            instance =form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "GeneratorReportChanged": None,
                        "showMessage": f"{instance.id} updated."
                    })
                }
            )
    
    
        form = GeneratorReportFormEdit(request.POST, instance=generator_report, generator=generator.id)
        return render(request, 'generator/partial/generator_report_form.html', {
        'form': form,
        'generator_report': generator_report,
        })
    
    form = GeneratorReportFormEdit(instance=generator_report, generator=generator.id)
    return render(request, 'generator/partial/generator_report_form.html', {
        'form': form,
         'generator_report': generator_report,
        })


@login_required(login_url='login')
def add_generator_report(request, id):
    generator = Generator.objects.get(id=id)
    form = GeneratorReportForm(generator= generator.id)
    if request.method == "POST":
        form = GeneratorReportForm(request.POST, request.FILES)
        if form.is_valid():
            
            instance = form.save()
                        
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "GeneratorReportChanged": None,
                         "showMessage": f"{instance.id} updated."

                        
                    })
                }
            )
        form = GeneratorReportForm(request.POST,request.FILES, generator=generator.id)   
       
        context = {'form':form}
        return render(request, 'generator/partial/generator_report_form.html', context)
    
    form = GeneratorReportForm(generator = generator.id)
    
    context = {'generator': generator, 'form':form }
    return render(request, 'generator/partial/generator_report_form.html', context)

@login_required(login_url='login')
def partial_generator_report(request, id):
    generator = Generator.objects.get(id=id)
    generator_report = Generator_Report.objects.filter(generator=generator).order_by('report_start_date')
    context = {'generator_report':generator_report }
    
    return render(request, 'generator/partial/generator_report.html', context)


@login_required(login_url='login')
def remove_generator_report(request, pk):
    generator_report = get_object_or_404(Generator_Report, pk=pk)
    generator_report.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "GeneratorReportChanged": None,
                "showMessage": f"{generator_report.id} deleted."
            })
        })


@login_required(login_url='login')
def generator_profile(request, id):
    generator = get_object_or_404(Generator,id=id)
    
    
    context = {'generator':generator,  }
    
    return render(request, 'generator/partial/generator_profile.html', context)


@login_required(login_url='login')
def download_gen_logsheet(request, id):
    document = get_object_or_404(Generator_Report, id=id)
    response = HttpResponse(document.gen_log_sheet, content_type='application/docx')
    response['Content-Disposition'] = f'attachment; filename="{document.gen_log_sheet}"'
    return response

 

@login_required(login_url='login')
def missing_report(request):
    user = request.user
    form = MissingLogForm()

    user = request.user
    form = MissingLogForm()

    if user.is_superuser:
        fff = Missing_Log.objects.values('field_office').distinct()
        form.fields['field_office'].choices = [('','')] +  [(ff.pk, ff.name) for ff in FieldOffice.objects.filter(id__in=fff).order_by('name')]
        form.fields['month'].choices =[(ff['month'], ff['month']) for ff in Missing_Log.objects.values('month').distinct()]
        form.fields['year'].choices =[(ff['year2'], ff['year2']) for ff in Missing_Log.objects.values('year2').distinct().order_by('-year2')]
    else:
  
        form.fields['field_office'].choices = [(ff.pk, ff) for ff in FieldOffice.objects.filter(id=user.profile.field_office.id)]
        form.fields['month'].choices =[(ff['month'], ff['month']) for ff in Missing_Log.objects.values('month').distinct()]
        form.fields['year'].choices =[(ff['year2'], ff['year2']) for ff in Missing_Log.objects.values('year2').distinct().order_by('-year2')]
    context = {'form':form }
    
    

    
    return render(request, 'report/missing_report.html', context)


def get_report_form(request):
    user = request.user
    form = MissingLogForm()

    user = request.user
    form = MissingLogForm()

    if user.is_superuser:
        fff = Missing_Log.objects.values('field_office').distinct()
        form.fields['field_office'].choices = [('All', 'All') for ff in FieldOffice.objects.filter(id__in=fff).order_by('name')]
        form.fields['month'].choices =[(ff['month'], ff['month']) for ff in Missing_Log.objects.values('month').distinct()]
        form.fields['year'].choices =[(ff['year2'], ff['year2']) for ff in Missing_Log.objects.values('year2').distinct().order_by('-year2')]
    else:
  
        form.fields['field_office'].choices = [(ff.pk, ff) for ff in FieldOffice.objects.filter(id=user.profile.field_office.id)]
        form.fields['month'].choices =[(ff['month'], ff['month']) for ff in Missing_Log.objects.values('month').distinct()]
        form.fields['year'].choices =[(ff['year2'], ff['year2']) for ff in Missing_Log.objects.values('year2').distinct().order_by('-year2')]
    context = {'form':form }
    

   
    return render(request, 'report/partial/report_form.html', context)
    


@login_required(login_url='login')
def generate_report(request):
     
     if request.method == 'POST':
        
        month = request.POST.get("month")
        year = request.POST.get("year")
        field_office = request.POST.get("field_office")
        print(month)
        if request.user.is_superuser and field_office == '':
            
            missing_report = Missing_Log.objects.filter(month=month, year2=year).order_by('generate_series','field_office')
            missing_expense = Missed_Expense.objects.filter(month=month, year=year).order_by('generate_series','field_office')
        else:
            missing_report = Missing_Log.objects.filter(field_office=field_office, month=month, year2=year).order_by('generate_series','field_office')
            missing_expense = Missed_Expense.objects.filter(field_office=field_office, month=month, year=year).order_by('generate_series','field_office')


        qs1 = missing_expense.filter(fleet_id = None)
        qs2 = missing_expense.filter(ownership = 'Rental', rental_and_tax = '', rental_fees = '')
        qs3 = missing_expense.filter(ownership = 'Mercy Corps', rental_and_tax = '', tax_insurance = '')
        qs4 = missing_expense.filter(Q(fuel_cost = '' ) | Q(cost_labour = '') | Q(cost_consumables = None) | Q(cost_spares = '')).exclude(fleet_id = None)
   
        
        missing_expense = qs1.union(qs2, qs3, qs4)
        total_missing = missing_report.count()
        total_expense = missing_expense.count()
        
        context = {'missing_report':missing_report, 'total_missing':total_missing, 'missing_expense':missing_expense, 'total_expense':total_expense}
       
            
    
        return render(request, 'report/partial/missing.html', context)
    
     return render(request, 'report/partial/missing.html')   
        

@login_required(login_url='login')
def aggregate_report(request):
    user = request.user
    form = MissingLogForm()

    user = request.user
    form = MissingLogForm()

    if user.is_superuser:
        fff = Log_Report.objects.values('field_office').distinct()
        form.fields['field_office'].choices = [('','')] + [(ff.pk, ff) for ff in FieldOffice.objects.filter(id__in=fff).order_by('name')]
        form.fields['month'].choices =[(ff['month_log'], ff['month_log']) for ff in Log_Report.objects.values('month_log').distinct().order_by('month_log')]
        form.fields['year'].choices =[(ff['year_log'], ff['year_log']) for ff in Log_Report.objects.values('year_log').distinct().order_by('-year_log')]
    else:
  
        form.fields['field_office'].choices = [(ff.pk, ff) for ff in FieldOffice.objects.filter(id=user.profile.field_office.id)]
        form.fields['month'].choices =[(ff['month_log'], ff['month_log']) for ff in Log_Report.objects.values('month_log').distinct().order_by('month_log')]
        form.fields['year'].choices =[(ff['year_log'], ff['year_log']) for ff in Log_Report.objects.values('year_log').distinct().order_by('-year_log')]
    
    context = {'form':form }
    
    
    return render(request, 'report/aggregate_report.html', context)



@login_required(login_url='login')
def dashboard(request):
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


def years(request):
    form = MissingLogForm(request.GET)
    return HttpResponse(form['year'])


@login_required(login_url='login')
def monthly_report(request):
     
     if request.method == 'POST':
        
        month = request.POST.get("month")
        year = request.POST.get("year")
        field_office = request.POST.get("field_office")
        

        if request.user.is_superuser and field_office == '':
            monthly_report = Log_Report.objects.filter( month_log=month, year_log=year).order_by('field_office')
            monthly_expense = Expense_Report.objects.filter( month_expense=month, year_expense=year).order_by('field_office')
        else:
            monthly_report = Log_Report.objects.filter(field_office=field_office, month_log=month, year_log=year).order_by('field_office')
            monthly_expense = Expense_Report.objects.filter(field_office=field_office, month_expense=month, year_expense=year).order_by('field_office')
            
        
        
        total_log = monthly_report.count()
        total_expense = monthly_expense.count()
        total_day_available =  sum(monthly_report.values_list('day_available', flat=True))
        total_day_total = sum(monthly_report.values_list('day_total', flat=True))

       
        
        context = {'monthly_report':monthly_report ,'monthly_expense': monthly_expense, 'total_log':total_log, 'total_expense':total_expense, 'total_day_available':total_day_available, 'total_day_total':total_day_total}
       
            
    
        return render(request, 'report/partial/log_monthly_report.html', context)
    
     return render(request, 'report/partial/log_monthly_report.html')   