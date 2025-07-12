from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
import json
from django.db.models import F
from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import QueryDict
import pandas as pd
from django.contrib.auth.decorators import login_required
from portfolio.models import Portfolio
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import ProgramForm, AddProgramAreaForm,EditProgramAreaForm, IndicatorForm, UserRoleForm, UserRoleFormE,UserRoleFormP, UserForm, TravelUserRoleForm, TravelUserRoleFormE

from .models import Program, ImplementationArea, Indicator, UserRoles, TravelUserRoles
from django.contrib.auth.models import User
from conceptnote.models import Icn, Activity
from django.db.models.functions import TruncMonth
from django.db.models import Q
from collections import defaultdict
from itertools import chain
from report.models import IcnReport, ActivityReport
from django.contrib.auth.decorators import permission_required
from user.models import Profile


@login_required(login_url='login')
def program_list(request):
    user = request.user
    if user.is_superuser:
        programs = Program.objects.all().order_by('-id')
    elif Program.objects.filter(users_role=user).count() == 1:
        program = Program.objects.get(users_role=user)
        return redirect('program_detail',pk=program.id) 
    
    else:
        programs = Program.objects.filter(users_role=user)
        
    
   
    context = {'programs': programs}
    return render(request, 'programs.html', context)


@login_required(login_url='login')
@permission_required("program.can_add_program", raise_exception=True)
def program_add(request): 
    # dictionary for initial data with  
    # field names as keys 
    form = ProgramForm()
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
           
            return redirect('program_detail',instance.pk) 
        
    context = {'form':form}
    return render(request, 'add_program.html', context)


@login_required(login_url='login')
def program_detail(request, pk):
    program = Program.objects.filter(pk=pk)
    x = Icn.objects.filter(program = pk).annotate(created_at_month=TruncMonth('created')).values('created_at_month').annotate(icn_count=Count('id')).order_by('created_at_month')
    y = Activity.objects.filter(icn__program = pk).annotate(created_at_month=TruncMonth('created')).values('created_at_month').annotate(acn_count=Count('id')).order_by('created_at_month')
  
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
    
   

    #all_request = all_request1.to_dict('list')
 
    total_icn  =  Icn.objects.filter(program_id = pk).count
    total_acn  =  Activity.objects.filter(icn__program_id = pk).count
    total_icn_app  =  Icn.objects.filter(program_id = pk, approval_status='100% Approved').count
    total_acn_app  =  Activity.objects.filter(icn__program_id = pk,approval_status='100% Approved').count
    total_report = IcnReport.objects.filter(Q(activityreport__activity__icn__program__in=program), Q(icn__program__in=program)).count 
   
   
   
    qsi = Icn.objects.filter(program_id = pk).only("title", "id","user","program_lead","technical_lead","finance_lead","status","approval_status","created","final_report_due_date","icnreport__approval_status").annotate(report = F('icnreport__approval_status'))
    qsa = Activity.objects.filter(icn__program_id = pk).only("title", "id", "user","program_lead","technical_lead","finance_lead","status","approval_status","created","final_report_due_date", "activityreport__approval_status").annotate(report = F('activityreport__approval_status'))
      
       
    conceptnotes = sorted(list(chain(qsi, qsa)), key=lambda instance: instance.created, reverse=True)
    
    

   
 
    # add the dictionary during initialization
  
    program = Program.objects.get(pk=pk)
    
    context = {'program':program, 'all_request':all_request, 'total_report':total_report,  'total_icn':total_icn, 'total_acn':total_acn, 'total_icn_app':total_icn_app, 'total_acn_app':total_acn_app,'conceptnotes': conceptnotes  }
    return render(request, 'program.html', context)


@login_required(login_url='login')
def program_profile(request, id):
    program = Program.objects.get(pk=id)
    context = {'program': program}
    return render(request, 'partial/program_profile.html', context)


@login_required(login_url='login')
@permission_required("program.can_change_program", raise_exception=True)
def program_edit(request, id): 
    # dictionary for initial data with  
    # field names as keys 
    program = Program.objects.get(pk=id)
    form = ProgramForm()

    if request.method == "POST":
       
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            instance = form.save()

            return redirect('program_detail',instance.pk) 
            
          

    form = ProgramForm(instance=program) 
    context = {'form':form}
    return render(request, 'add_program.html', context)

@login_required(login_url='login')
@permission_required("program.can_change_program", raise_exception=True)
def program_profile_edit(request, id):
    program = Program.objects.get(pk=id)
    if request.method == "POST":
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            instance =form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ProgramListChanged": None,
                        "showMessage": f"{instance.title} updated."
                    })
                }
            )
        else:
            form = ProgramForm(instance=program)
            return render(request, 'partial/program_profile_form.html', {
            'form': form,
            'program': program,
        })
    form = ProgramForm(instance=program)
    return render(request, 'partial/program_profile_form.html', {
            'form': form,
            'program': program,
        })

@login_required(login_url='login')       
def program_list_filter(request):
    query = request.GET.get('search', '')
   

    all_programs= Program.objects.all().order_by('-id')
    if query:
        qs1 = Program.objects.filter(title__icontains=query)
        qs2 = Program.objects.distinct().filter(portfolio__title__icontains=query)
        
        
        programs = qs1.union(qs2).order_by('id')
       
    else:
        programs = Program.objects.all().order_by('-id')

    context = {'programs': programs, 'count': all_programs.count()}
    return render(request, 'partial/program_list.html', context)  

   
 
@login_required(login_url='login')
@permission_required("program.can_add_implementationarea", raise_exception=True)
def region(request, id):
    program = get_object_or_404(Program, id=id)
    if request.method == "POST":
        form = AddProgramAreaForm(request.POST, program=program)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "areaListChanged": None,
                        "showMessage": f"{instance.woreda} added."
                    })
                })
        form = AddProgramAreaForm(request.POST, program=program)
             
        context = {'form': form}
        return render(request, 'partial/area_form.html', context)
            
    
    form = AddProgramAreaForm(program=program)
    context = {'form': form}
    
    return render(request, 'partial/area_form.html', context)

def zones(request):
    form = AddProgramAreaForm(request.GET)
    return HttpResponse(form['zone'])


   

def woredas(request):
    form = AddProgramAreaForm(request.GET)
    return HttpResponse(form['woreda'])

@login_required(login_url='login')
@permission_required("program.can_change_implementationarea", raise_exception=True)
def area_edit_form(request, pk):
    area = get_object_or_404(ImplementationArea, pk=pk)    
    if request.method == "GET":
        iarea = get_object_or_404(ImplementationArea, pk=int(pk))
        form = EditProgramAreaForm(instance=iarea)
        context = {'area': area, 'form': form }
        return render(request, 'partial/area_form_edit.html', context)

    elif request.method == "PUT":
        area = get_object_or_404(ImplementationArea, pk=int(pk))
        data = QueryDict(request.body).dict()
        form = EditProgramAreaForm(data, instance=area)
        if form.is_valid():
            instance=form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "areaListChanged": None,
                        "showMessage": f"{instance.woreda} updated."
                    })
                }
            )
        
        
        form = EditProgramAreaForm(data, instance=area)
        context = {'area': area, 'form': form }
        return render(request, 'partial/area_form_edit.html', context)
     
       



@login_required(login_url='login')
@permission_required("program.can_change_userroles", raise_exception=True)
def edit_user_role(request, uid):
   
    user = User.objects.get(pk=uid)
   
    
   
        
    if request.method == "PUT":
        user = User.objects.get(pk=uid)
        data = QueryDict(request.body).dict()
        form = UserRoleFormE(data, instance=user, user=user)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserListChanged": None,
                        "showMessage": f"{instance.username} updated."
                    })
                })
        
        form = UserRoleFormE(instance=user, user=user) 
        context = {'form': form}
        return render(request, 'partial/edit_user_role.html', context)
    
    form = UserRoleFormE(instance=user, user=user) 
    context = {'form':form}
    return render(request, 'partial/edit_user_role.html', context)



@login_required(login_url='login')
def indicator_list(request, id):
    return render(request, 'partial/indicator_list.html', {
        'indicators': Indicator.objects.filter(program_id=id),
    })


@login_required(login_url='login')
@permission_required("program.can_add_indicator", raise_exception=True)
def add_indicator(request, id):
    if request.method == "POST":
        form = IndicatorForm(request.POST)
        if form.is_valid():
            indicator = form.save(commit=False)
            indicator.program = get_object_or_404(Program, pk=id)
            indicator.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "IndicatorListChanged": None,
                        "showMessage": f"{indicator.indicator_title} added."
                    })
                })
    else:
        form = IndicatorForm()
    return render(request, 'partial/indicator_form.html', {
        'form': form,
    })

@login_required(login_url='login')
@permission_required("program.can_change_indicator", raise_exception=True)
def edit_indicator(request, pk):
    indicator = get_object_or_404(Indicator, pk=pk)
    if request.method == "POST":
        form = IndicatorForm(request.POST, instance=indicator)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "IndicatorListChanged": None,
                        "showMessage": f"{indicator.indicator_title} updated."
                    })
                }
            )
    else:
        form = IndicatorForm(instance=indicator)
    return render(request, 'partial/indicator_form.html', {
        'form': form,
        'indicator': indicator,
    })


@login_required(login_url='login')
@permission_required("program.can_delete_indicator", raise_exception=True)
def remove_indicator(request, pk):
    indicator = get_object_or_404(Indicator, pk=pk)
    indicator.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "IndicatorListChanged": None,
                "showMessage": f"{indicator.indicator_title} deleted."
            })
        })


@login_required(login_url='login')
def user_list(request, id):
    program = get_object_or_404(Program, pk=id)
    program_users = UserRoles.objects.filter(program=program)
    return render(request, 'partial/user_list_program.html', {
        'users': program_users,
    })

@login_required(login_url='login')
@permission_required("program.can_add_userroles", raise_exception=True)
def add_user(request, id):
    program = Program.objects.get(pk=id)
    if request.method == "POST":
        program = Program.objects.get(pk=id)
        form = UserRoleForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.program = program
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserListChanged": None,
                        "showMessage": f"{instance.user} updated."
                    })
                })
    else:
        form = UserRoleForm(program=program)
    return render(request, 'partial/user_role.html', {
        'form': form,
        
    })

@login_required(login_url='login')
def area_list(request, id):
    return render(request, 'partial/area_list.html', {
        'areas': ImplementationArea.objects.filter(program_id=id),
    })

@login_required(login_url='login')
@permission_required("program.can_change_userroles", raise_exception=True)
def update_user_roles(request, id):
    
    user_role = UserRoles.objects.get(pk=id)
    user = get_object_or_404(User, pk=user_role.user_id)
    if request.method == "PUT":
        user_role = UserRoles.objects.get(pk=id)
       
            
        data = QueryDict(request.body).dict()
        if user_role.is_pacn_program_approver == True or user_role.is_pcn_program_approver == True:
             form = UserRoleFormP(data, instance=user_role, user=user)
        else:
             form = UserRoleFormE(data, instance=user_role, user=user)
        
       
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserListChanged": None,
                        "showMessage": f"{instance.user } updated."
                    })
                })
        
        if user_role.is_pacn_program_approver == True or user_role.is_pcn_program_approver == True:
            form = UserRoleFormP(instance=user_role, user=user)
        else:
            form = UserRoleFormE(instance=user_role, user=user)
            
        context = {'form': form}
        return render(request, 'partial/edit_user_role.html', context)
    
    else:
        if user_role.is_pacn_program_approver == True or user_role.is_pcn_program_approver == True:
            form = UserRoleFormP(instance=user_role, user=user)
        else:
            form = UserRoleFormE(instance=user_role, user=user)

        return render(request, 'partial/edit_user_role.html', {
        'form': form,
        'user_role': user_role,
    })

@login_required(login_url='login')
@permission_required("program.can_delete_userroles", raise_exception=True)
def remove_user_role(request, pk):
    user_role = get_object_or_404(UserRoles, pk=pk)
    user_role.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "UserListChanged": None,
                "showMessage": f"{user_role.user} deleted."
            })
        })



@login_required(login_url='login')
@permission_required("program.can_delete_implementationarea", raise_exception=True)
def delete_area(request, pk):
    area = get_object_or_404(ImplementationArea, pk=pk)
    area.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "areaListChanged": None,
                "showMessage": f"{area.woreda} deleted."
            })
        })


@login_required(login_url='login')
@permission_required("portfolio.can_add_portfoilio", raise_exception=True)
def newportfolio(request):
    portfolio = Portfolio.objects.all()
    form = ProgramForm(portfolio=portfolio)
   
    return HttpResponse(form['portfolio'])

@login_required(login_url='login')
@permission_required("program.can_add_userroles", raise_exception=True)
def add_travel_user(request, id):
    program = Program.objects.get(pk=id)
    if request.method == "POST":
        program = Program.objects.get(pk=id)
        form = TravelUserRoleForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.program = program
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "TravelUserListChanged": None,
                        "showMessage": f"{instance.profile} updated."
                    })
                })
    else:
        form = TravelUserRoleForm(program=program)
    return render(request, 'partial/travel_user_role.html', {
        'form': form,
        
    })

@login_required(login_url='login')
def user_travel_list(request, id):
    program = get_object_or_404(Program, pk=id)
    travel_user_list = TravelUserRoles.objects.filter(program=program)
    return render(request, 'partial/travel_user_list_program.html', {
        'travel_user_list': travel_user_list,
    })


@login_required(login_url='login')
@permission_required("program.can_change_userroles", raise_exception=True)
def update_travel_user_roles(request, id):
    tuser_role = TravelUserRoles.objects.get(pk=id)
    profile = get_object_or_404(Profile, pk=tuser_role.profile_id)
    program = get_object_or_404(Program, pk=tuser_role.program_id)

    if request.method == "POST":
       
        form = TravelUserRoleFormE(request.POST, instance=tuser_role, profile=profile)
     
        if form.is_valid():
            instance = form.save()
           
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "TravelUserListChanged": None,
                        "showMessage": f"{instance.profile} updated."
                    })
                })
    
    form = TravelUserRoleFormE(instance=tuser_role, profile=profile)
    return render(request, 'partial/travel_user_role.html', {
        'form': form,'tuser_role':tuser_role
        
    })

@login_required(login_url='login')
@permission_required("program.can_delete_userroles", raise_exception=True)
def remove_travel_user_role(request, pk):
    tuser_role = get_object_or_404(TravelUserRoles, pk=pk)
    tuser_role.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "TravelUserListChanged": None,
                "showMessage": f"{tuser_role.profile} deleted."
            })
        })