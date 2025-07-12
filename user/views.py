from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
import json
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from program.models import Program, UserRoles
from conceptnote.models import Icn, Activity
from report.models import IcnReport, ActivityReport
import json
from django.db.models import Max, Avg,Sum,Count
from django.db.models import Q
from collections import defaultdict
from itertools import chain
from django import template
from easyaudit.models import CRUDEvent, RequestEvent, LoginEvent
from .forms import LoginForm, ProfileFormAdd
from .models import Profile
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import datetime, date

from dateutil.relativedelta import relativedelta




@login_required(login_url='login')
def user(request):
    user = User.objects.get(pk=request.user.id)
    
    current_date = date.today()
    start_date =  current_date - relativedelta(months=1)
    end_date = date.today()

    qs2 = LoginEvent.objects.filter(user_id=request.user.id,  datetime__date__gte=start_date, datetime__date__lte=end_date).order_by("datetime__date").values('datetime__date').annotate(count_login=Count('id', distinct=True))
  
  
    
   
    

    all_request = qs2
    
  
    
    context = {'user':user,'all_request':all_request, }
    return render(request, 'user/accounts.html', context)



@login_required(login_url='login')
def user_activity(request):
    if request.GET.get('reservation', ''):
        
        query = request.GET.get('reservation', '')
        query = query.split("-")
        #for q in query:
        start_date = query[0].strip()
        end_date = query[1].strip()
       
        start_date = datetime.strptime(start_date, '%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%m/%d/%Y')
        
      
       
       
        qs2 = LoginEvent.objects.filter(user_id=request.user.id,  datetime__date__gte=start_date, datetime__date__lte=end_date).order_by("datetime__date").values('datetime__date').annotate(count_login=Count('id', distinct=True))
    else:
        current_date = date.today()
        last_month_filter =  current_date - relativedelta(months=1)
    
       
      
        qs2 = LoginEvent.objects.filter(user_id=request.user.id, datetime__gte=last_month_filter).order_by("datetime__date").values('datetime__date').annotate(count_login=Count('id',distinct=True))
    


    
    

    all_request = qs2

    context = {'all_request':all_request, }
    return render(request, 'user/partial/user_activity.html', context)



     

@login_required(login_url='login')
def activity_filter(request):
    query = request.GET.get('dates', '')
    print(query)
    print("hye")
    
    return render(request, 'user/partial/admin_boundary.html')

  
class Login(LoginView):
    template_name = 'user/registration/login.html'
    

class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'user/registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.is_active = False
        instance.save()  # save the user
        return super().form_valid(form)



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'user/registration/password_reset.html'
    email_template_name = 'user/registration/password_reset_email.html'
    subject_template_name = 'user/registration/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')
    



# Create your views here.
@login_required(login_url='login')
def userprofile(request):
 
    user = User.objects.get(pk=request.user.id)
    context = {'user': user}
    return render(request, 'user/partial/user_profile.html', context)

@login_required(login_url='login')
def add_profile(request): 
    user =User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile, user=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserprofileChanged": None,
                        "showMessage": f"{user.email} updated."
                    })
                })
        else:
            user_form = CustomUserChangeForm(instance=user)
            profile_form = ProfileForm(instance=user.profile, user=request.user)
            
    else:
       
        profile_form = ProfileForm(instance=user.profile, user=request.user)
       
            
        user_form = CustomUserChangeForm(instance=user)
        return render(request, 'user/profile_form.html', {
        'profile_form': profile_form, 'user_form':user_form
    })
    return render(request, 'user/profile_form.html', {
         'user_form' :CustomUserChangeForm(instance=user),'profile_form': ProfileForm(user=request.user)})

@login_required(login_url='login')
def user_profile(request): 
    
    user = User.objects.get(pk=request.user.id)
    context = {'user': user}
        
    
    return render(request, 'user/partial/user_profile.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_success')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/password_change_form.html', {
        'form': form
    })
def change_success(request):
    return render(request, 'user/partial/password_change_success.html')

@login_required(login_url='login')
def newuserprofile(request): 
    user =User.objects.get(pk=request.user.id)
    if request.method == 'POST':
       
        profile_form = ProfileFormAdd(request.POST)

        if profile_form.is_valid():
            instance = profile_form.save(commit=False)
            instance.user = user
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "UserprofileChanged": None,
                        "showMessage": f"{user.email} updated."
                    })
                })
    
    profile_form = ProfileFormAdd(request.POST, user=user)
    context = {'profile_form':profile_form}
    return render(request, 'user/partial/profile_form_new.html', context)

@login_required(login_url='login')
def user_program_roles(request):
    user = get_object_or_404(User, pk=request.user.id)
    program_users = UserRoles.objects.filter(user=user)
    return render(request, 'user/partial/user_program_role.html', {
        'program_users': program_users,
    })


def user_conceptnotes(request):
    
    user = User.objects.filter(username=request.user)
   
    userroles = UserRoles.objects.filter(user__in=user)
    qsi =  Icn.objects.filter(Q(user__in=user) | Q(program_lead__in=userroles) | Q(technical_lead__in=userroles)| Q(finance_lead__in=userroles)|Q(mel_lead__in=userroles)|Q(icnreport__user__in=user) | Q(icnreport__program_lead__in=userroles) | Q(icnreport__technical_lead__in=userroles)| Q(icnreport__finance_lead__in=userroles)|Q(icnreport__mel_lead__in=userroles)).exclude(approval_status='100% Approved', icnreport__approval_status='100% Approved')
    qsa = Activity.objects.filter(Q(user__in=user) | Q(program_lead__in=userroles) | Q(technical_lead__in=userroles)| Q(finance_lead__in=userroles)|Q(mel_lead__in=userroles)|Q(activityreport__user__in=user) | Q(activityreport__program_lead__in=userroles) | Q(activityreport__technical_lead__in=userroles)| Q(activityreport__finance_lead__in=userroles)|Q(activityreport__mel_lead__in=userroles)).exclude(approval_status='100% Approved', activityreport__approval_status='100% Approved')
    
       
    
    return render(request, 'user/partial/conceptnotes.html', {
        'qsi': qsi,'qsa':qsa
    })




  

