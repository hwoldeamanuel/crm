from django.shortcuts import render
from django.core.files.uploadedfile import TemporaryUploadedFile
import json
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse 
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import QueryDict
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from .models import Icn, Activity, ActivityImpact,ActivityImplementationArea,  Indicator, IcnImplementationArea,  Impact, IcnSubmit, Document, Icn_Approval, IcnSubmitApproval_P, IcnSubmitApproval_F, IcnSubmitApproval_M,IcnSubmitApproval_T, ActivityDocument, ActivitySubmit, ActivitySubmitApproval_F,ActivitySubmitApproval_P, ActivitySubmitApproval_M, ActivitySubmitApproval_T, Disaggregate
from .forms import IcnForm, ActivityForm,ImpactForm, ActivityImpactForm, ActivityAreaFormE, IcnAreaFormE, IcnSubmitForm,  IcnDocumentForm, IcnApprovalTForm, IcnApprovalFForm, IcnApprovalPForm, IcnApprovalMForm,ActivitySubmitForm, ActivityDocumentForm, ActivityApprovalFForm, ActivityApprovalPForm,ActivityApprovalTForm, ActivityApprovalMForm, DisaggregateForm
from program.models import  Program,  ImplementationArea
from django.http import QueryDict
from django.conf import settings
from app_admin.models import Country , Region , Zone , Woreda

from portfolio.models import Portfolio
from django.conf import settings

from django.forms.models import modelformset_factory
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Max, Avg,Sum,Count
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from django.template import Context
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from render_block import render_block_to_string
from django_htmx.http import HttpResponseClientRedirect
from django_htmx.http import HttpResponseClientRefresh
from app_admin.models import Approvalt_Status, Approvalf_Status, Submission_Status
from mimetypes import guess_type
from os.path import basename
    # ...
    
# Create your views here.

@login_required(login_url='login')
def conceptnotes(request):
    
    user = request.user
    program = Program.objects.filter(users_role=user)
   
  
    if user.is_superuser:
        icns = Icn.objects.all()
    else:
        icns = Icn.objects.filter(program__in=program).order_by('-id')


    context = {'icns':icns}
    
    return render(request, 'interventions.html', context)

@login_required(login_url='login')
def icn_add(request): 
    if request.method == "POST":
        form = IcnForm(request.POST,request.FILES, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
           
            selected_woredas = request.POST.getlist("iworeda")
            selected_co_agency = request.POST.getlist("ilead_co_agency")
            items_woreda = ImplementationArea.objects.filter(id__in=selected_woredas)
            items_co_agency = Portfolio.objects.filter(id__in=selected_co_agency)
            instance.save()
            instance.iworeda.add(*items_woreda)
            instance.ilead_co_agency.add(*items_co_agency)
            return redirect('icn_detail',instance.pk) 
        
        
        form = IcnForm(request.POST,request.FILES, user=request.user)   
       
        context = {'form':form}
        return render(request, 'intervention_step_profile_new.html', context)
    
    form = IcnForm(user=request.user)   
    
    context = {'form':form}
    return render(request, 'intervention_step_profile_new.html', context)

@login_required(login_url='login')
def icn_edit(request, id): 
    icn = Icn.objects.get(pk=id)
    
    if request.method == "POST":
       
        form = IcnForm(request.POST,request.FILES, instance=icn, user=request.user)
        if form.is_valid():
            instance = form.save()
            return redirect('icn_detail',instance.pk) 
        
        form = IcnForm(request.POST, request.FILES, instance=icn, user=request.user) 
        context = {'form':form}
        return render(request, 'intervention_step_profile_edit.html', context)
            
    elif request.method == "GET" and icn.status == False:    

        form = IcnForm(instance=icn,  user=request.user) 
        context = {'form':form, 'icn':icn}
        return render(request, 'intervention_step_profile_edit.html', context)
    else:
        return HttpResponseRedirect(request.path_info)
                
@login_required(login_url='login') 
def icn_step_impact(request, id):
     icn = Icn.objects.get(id=id)
     
     impacts= Impact.objects.filter(icn_id=id)
     context = {'icn':icn, 'impacts': impacts}
     return render(request, 'intervention_step_impact.html', context)

@login_required(login_url='login') 
def icn_step_submission(request, id):
    icn = get_object_or_404(Icn, pk=id)
    context ={}
 
    # add the dictionary during initialization
    icn = Icn.objects.get(pk=id)
    if IcnSubmit.objects.filter(icn_id=icn.id).exists():
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        context = {'icn':icn, 'icnsubmit':icnsubmit}
    else:
        context = {'icn':icn}
    return render(request, 'intervention_step_submission.html', context)

@login_required(login_url='login')
def current_submit_list(request, id):
    
    icn = Icn.objects.get(pk=id)
    if IcnSubmit.objects.filter(icn_id=icn.id).exists():
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        context = {'icn':icn, 'icnsubmit':icnsubmit}
    else:
        context = {'icn':icn}
  
    
    return render(request, 'partial/current_submit_list.html', context)

@login_required(login_url='login') 
def icn_step_approval(request, id):
    icn = get_object_or_404(Icn, pk=id)
    context ={}
 
    # add the dictionary during initialization
    icn = Icn.objects.get(pk=id)
    if IcnSubmit.objects.filter(icn_id=icn.id).exists():
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        context = {'icn':icn, 'icnsubmit':icnsubmit}
    else:
        context = {'icn':icn}
    return render(request, 'intervention_step_approval.html', context)


@login_required(login_url='login') 
def activity_step_approval(request, id):
    activity = get_object_or_404(Activity, pk=id)
    context ={}
 
    # add the dictionary during initialization
    activity = Activity.objects.get(pk=id)
    if ActivitySubmit.objects.filter(activity_id=activity.id).exists():
        activitysubmit = ActivitySubmit.objects.filter(activity_id=activity.id).latest('id')
        context = {'activity':activity, 'activitysubmit':activitysubmit}
    else:
        context = {'activity':activity}
    return render(request, 'activity_step_approval.html', context)

@login_required(login_url='login') 
def icn_detail(request, pk):
    
    context ={}
    user = request.user
    program = Program.objects.filter(users_role=user)
   
   
    # add the dictionary during initialization
    if user.is_superuser:
        icn = get_object_or_404(Icn, pk=pk)
    else:
        icn = get_object_or_404(Icn, pk=pk,program__in=program)
    
    form = IcnForm(instance=icn,  user=request.user) 
    for fieldname in form.fields:
        form.fields[fieldname].disabled  = True
    if IcnSubmit.objects.filter(icn_id=icn.id).exists():
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        context = {'icn':icn, 'icnsubmit':icnsubmit, 'form':form}
    else:
        context = {'form':form, 'icn':icn}
    
    #icnsubmit= IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
    #icnsubmit = get_object_or_404(IcnSubmit, icn_id=icn.id).latest('id')


    return render(request, 'intervention_step_profile_detail.html', context)

@login_required(login_url='login') 
def icn_step_report(request, id):
    icn = Icn.objects.get(pk=id)
    if IcnSubmit.objects.filter(icn_id=icn.id).exists():
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        context = {'icn':icn, 'icnsubmit':icnsubmit}
    else:
        context = {'icn':icn}
    return render(request, 'intervention_step_report.html', context)


def izones(request):
    form = IcnAreaFormE(request.GET)
    return HttpResponse(form['zone'])


    
   

def iworedas(request):
    form = IcnForm(request.GET)
    return HttpResponse(form['iworeda'])

@login_required(login_url='login')
def iregion(request, id):
    #icn = get_object_or_404(IcnImplementationArea, pk=id)
    if request.method == "POST":
        form = IcnAreaFormE(request.POST or none)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.icn = Icn.objects.get(pk=id)
            instance.user = request.user
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "IareaListChanged": None,
                        "showMessage": f"{instance.woreda} added."
                    })
                })
        form = IcnAreaFormE(request.POST)
        context = {'form': form}
    
        return render(request, 'iarea_form.html', context)
    
    form = IcnAreaFormE()
    context = {'form': form}
    
    return render(request, 'iarea_form.html', context)

@login_required(login_url='login') 
def icn_new(request): 
    form = IcnForm(user=request.user)
    if request.method == "POST":
        form = IcnForm(request.POST, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('icn_detail',instance.pk) 
        
    context = {'form':form}
    return render(request, 'intervention_add.html', context)

@login_required(login_url='login') 
def iarea_edit_form(request, pk):
    iarea = get_object_or_404(IcnImplementationArea, pk=pk)
    icn = iarea.icn
    
    if request.method == "GET":
        iarea = get_object_or_404(IcnImplementationArea, pk=int(pk))
        form = IcnAreaFormE(instance=iarea)
        context = {'iarea': iarea, 'form': form }
        return render(request, 'iarea_edit_form.html', context)


    elif request.method == "PUT":
        iarea = get_object_or_404(IcnImplementationArea, pk=int(pk))
        data = QueryDict(request.body).dict()
        form = IcnAreaFormE(data, instance=iarea)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "IareaListChanged": None,
                        "showMessage": f"{instance.woreda} updated."
                    })
                }
            )
     



@login_required(login_url='login') 
def idelete_area(request, pk):
    area = get_object_or_404(IcnImplementationArea, pk=pk)
    icn = area.icn_id
    area.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "IareaListChanged": None,
                "showMessage": f"{area.woreda} deleted."
            })
        })

@login_required(login_url='login') 
def icn_delete(request, pk):
    icn = get_object_or_404(Icn, pk=pk)
   
    icn.delete()
    user = request.user
    if user.is_superuser:
        icns = Icn.objects.all()
    else:
        program = Program.objects.filter(users_role=user)
        icns = Icn.objects.filter(program__in=program).order_by('-id')
   
        
    
    context = {'icns': icns, }
    return render(request, 'partial/icn_list.html', context)

@login_required(login_url='login') 
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
   
    activity.delete()
    
    user = request.user
    if user.is_superuser:
        activities = Activity.objects.all()
    else:
        program = Program.objects.filter(users_role=user)
        activities = Activity.objects.filter(program__in=program).order_by('-id')

    context = {'activities': activities, 'count': activities.count()}
    return render(request, 'partial/activity_list.html', context)
       
  

@login_required(login_url='login') 
def icn_submit_form(request, id, sid): 
    icn = get_object_or_404(Icn, pk=id)
    
    form = IcnSubmitForm(user=request.user,icn=icn.id, sid=sid)
    
    if request.method == "POST":
        form = IcnSubmitForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.icn = icn
            
            instance.user = request.user
            instance.save()
            #document = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
            #document_i = Document.objects.filter(icn=instance.icn, user=icn.user).count()+1
            
            icnsubmit = get_object_or_404(IcnSubmit, pk=instance.pk)
            #Document.objects.create(user = icn.user, document = instance.document,  icn=instance.icn, description = document_i)
          
            if icnsubmit.submission_status_id == 2:
                Icn.objects.filter(pk=id).update(status=True)
                Icn.objects.filter(pk=id).update(approval_status="Pending Approval")
                
                IcnSubmitApproval_T.objects.create(user = icn.technical_lead,submit_id = instance, document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                IcnSubmitApproval_M.objects.create(user = icn.mel_lead,submit_id = instance, document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                IcnSubmitApproval_P.objects.create(user = icn.program_lead,submit_id = instance,document = instance.document, approval_status=Approvalf_Status.objects.get(id=1))
                IcnSubmitApproval_F.objects.create(user = icn.finance_lead,submit_id = instance,document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                send_icn_notify(icn.id, 12, instance.document_id)
                           
             
            elif icnsubmit.submission_status_id == 1:
                Icn.objects.filter(pk=id).update(status=False)
                Icn.objects.filter(pk=id).update(approval_status="Pending Submission")
               
                icn =  get_object_or_404(Icn, id=icnsubmit.icn_id)
                send_icn_notify(icn.id, 11, instance.document_id)
                
               
            return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "SubmitApprovalListChanged": None,
                    "showMessage": f"{instance.id} added."
                })
            })
      
    context = {'form':form, 'icn':icn, 'sid':sid}
    return render(request, 'icn_submit_form copy.html', context)


@login_required(login_url='login') 
def icn_submit_detail(request, pk):
    
    context ={}
 
    # add the dictionary during initialization
  
    icnsubmit = IcnSubmit.objects.get(pk=pk,  submission_status=2)
    
   

    context = {'icnsubmit':icnsubmit}

    return render(request, 'icnsubmit_detail.html', context)


@login_required(login_url='login') 
def icn_approvalt(request, id, did):
     
    icnsubmitApproval_t = get_object_or_404(IcnSubmitApproval_T, submit_id_id=id)
    icnsubmit = get_object_or_404(IcnSubmit, pk=id)
    did=did
    icn =  get_object_or_404(Icn, id=icnsubmit.icn_id)
    
    if request.method == "GET":
        form = IcnApprovalTForm(instance=icnsubmitApproval_t, did=did, icn = icn.id, user = request.user)
                    
        context = {'icnsubmitapproval_t':icnsubmitApproval_t, 'form': form, 'icn':icn, 'did':did}
        return render(request, 'icn_approval_tform.html', context)
    
    elif request.method == "PUT":
        icnsubmitApproval_t = get_object_or_404(IcnSubmitApproval_T, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = IcnApprovalTForm(data, instance=icnsubmitApproval_t, did=did,user = request.user )
        if form.is_valid():
            instance = form.save()
            icnsubmit = get_object_or_404(IcnSubmit, pk=id)
            update_approval_status(icnsubmit.id)
            icn =  get_object_or_404(Icn, id=icnsubmit.icn_id)
            send_icn_notify(icn.id, 2, instance.document_id)
                      
            context = {'icn':icn, 'icnsubmit':icnsubmit , 'did':did}
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'icn_approval_tform.html', {'form':form, 'did':did})
  
@login_required(login_url='login') 
def icn_approvalm(request, id, did):
     
    icnsubmitApproval_m = get_object_or_404(IcnSubmitApproval_M, submit_id_id=id)
    icnsubmit = get_object_or_404(IcnSubmit, pk=id)
    did=did
    icn =  get_object_or_404(Icn, id=icnsubmit.icn_id)
     
    if request.method == "GET":
        form = IcnApprovalMForm(instance=icnsubmitApproval_m, did=did, icn=icn.id, user= request.user )
        context = {'icnsubmitapproval_m':icnsubmitApproval_m, 'form': form, 'icn':icn, 'did':did}
        return render(request, 'icn_approval_mform.html', context)
    
    elif request.method == "PUT":
        icnsubmitApproval_m = get_object_or_404(IcnSubmitApproval_M, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = IcnApprovalMForm(data, instance=icnsubmitApproval_m, did=did, user = request.user)
        if form.is_valid():
            instance = form.save()
            icnsubmit = get_object_or_404(IcnSubmit, pk=id)
            update_approval_status(icnsubmit.id)
            icn =  get_object_or_404(Icn, id=icnsubmit.icn_id)
            send_icn_notify(icn.id, 3, instance.document_id)
           
            context = {'icn':icn, 'icnsubmit':icnsubmit , 'did':did}
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'icn_approval_mform.html', {'form':form, 'did':did})

@login_required(login_url='login')
def icn_approvalp(request, id, did):
    
    icnsubmitApproval_p = get_object_or_404(IcnSubmitApproval_P, submit_id_id=id)
    icnsubmit = get_object_or_404(IcnSubmit, pk=id)
    did = did
    icn =  get_object_or_404(Icn, id=icnsubmit.icn_id)
          
    if request.method == "GET":
        form = IcnApprovalPForm(instance=icnsubmitApproval_p, icn=icn.id, user=request.user, did=did)
        context = {'icnsubmitapproval_p':icnsubmitApproval_p, 'form': form, 'icn':icn, 'did':did }
        return render(request, 'icn_approval_pform.html', context)
    
    elif request.method == "PUT":
        icnsubmitApproval_p = get_object_or_404(IcnSubmitApproval_P, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = IcnApprovalPForm(data, instance=icnsubmitApproval_p, did=did)
        if form.is_valid():
            instance = form.save()
            icnsubmit = get_object_or_404(IcnSubmit, pk=id)
            update_approval_status_final(icnsubmit.id)
            icn =  get_object_or_404(Icn, id=icnsubmit.icn_id)
            
            send_icn_notify(icn.id, 5, instance.document_id)

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'icn_approval_pform.html', {'form':form, 'did':did})


@login_required(login_url='login') 
def icn_approvalf(request, id, did):
    icnsubmitApproval_f = get_object_or_404(IcnSubmitApproval_F, submit_id_id=id)
    icnsubmit = get_object_or_404(IcnSubmit, pk=id)
    did = did
    icn =  get_object_or_404(Icn, id=icnsubmit.icn_id)
           
    if request.method == "GET":
        form = IcnApprovalFForm(instance=icnsubmitApproval_f, did=did, icn=icn.id, user=request.user)
            
        context = {'icnsubmitapproval_f':icnsubmitApproval_f, 'form': form, 'icn':icn, 'did':did }
        return render(request, 'icn_approval_fform.html', context)
    
    elif request.method == "PUT":
        icnsubmitApproval_f = get_object_or_404(IcnSubmitApproval_F, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = IcnApprovalFForm(data, instance=icnsubmitApproval_f, did=did)
        if form.is_valid():
            instance = form.save()
            icnsubmit = get_object_or_404(IcnSubmit, id=id)
            update_approval_status(icnsubmit.id)
            icn =  get_object_or_404(Icn, id=icnsubmit.icn_id)
            send_icn_notify(icn.id, 4, instance.document_id)

            context = {'icn':icn, 'icnsubmit':icnsubmit, 'did':did }
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'icn_approval_fform.html', {'form':form, 'did':did})
    
@login_required(login_url='login')
def icn_submit_approval(request, pk):
    icn = get_object_or_404(Icn, pk=pk)
    context ={}
 
    # add the dictionary during initialization
    icn = Icn.objects.get(pk=pk)
    if IcnSubmit.objects.filter(icn_id=icn.id).exists():
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        context = {'icn':icn, 'icnsubmit':icnsubmit}
    else:
        context = {'icn':icn}
    

    return render(request, 'submit_approval.html', context)

@login_required(login_url='login') 
def icn_submit_list(request, id):
    context ={}
 
    # add the dictionary during initialization
  
    icn = Icn.objects.get(pk=id)
    if IcnSubmit.objects.filter(icn_id=icn.id).exists():
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        context = {'icn':icn, 'icnsubmit':icnsubmit}
    else:
        context = {'icn':icn}

    return render(request, 'partial/submit_list.html', context)


@login_required(login_url='login') 
def icn_submit_document(request, id):
    context ={}
    icn = get_object_or_404(Icn, pk=id)
    dform = IcnDocumentForm()
    if Document.objects.filter(icn_id=icn.id).exists():
        major = Document.objects.filter(icn=icn.id, user=icn.user).count() 
        last_initiator_doc = Document.objects.filter(icn=icn.id, user=icn.user).latest('id') 
        minor = Document.objects.filter(icn=icn.id, id__gt=last_initiator_doc.id).exclude(user=icn.user)
        minor = minor.count()
    else:
        major = 0
        minor = 0

    context = {'dform':dform}
    if request.method == 'POST':
        dform = IcnDocumentForm(request.POST, request.FILES)
        if dform.is_valid():
            instance = dform.save(commit=False)
            instance.icn = icn
            instance.user = request.user
            if instance.user == icn.user:
                 major = major + 1
                 minor = 0
            else:
                 major = major 
                 minor = minor + 1
              
            instance.ver = "%s%s%s" %(major,'.',minor)

            instance.save()
            
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "DocListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
            
    else:
       dform = IcnDocumentForm()
       context = {'dform':dform}
       return render(request, 'partial/icn_document_form copy.html', context)
           
            
       
   
@login_required(login_url='login')       
def document_list(request, id):
    documents = Document.objects.filter(icn_id=id)
    context = {'documents':documents}
           
          
    
    return render(request,'partial/icn_document_list.html', context)
       

@login_required(login_url='login')
def download(request, id):
    document = get_object_or_404(Document, id=id)
    response = HttpResponse(document.document, content_type='application/docx')
    response['Content-Disposition'] = f'attachment; filename="{document.document}"'
    return response

@login_required(login_url='login')
def search_results_view(request):
    user = request.user
    program = Program.objects.filter(users_role=user)
   
    icns = Icn.objects.filter(program__in=program).order_by('-id')
    query = request.GET.get('search', '')
    

    all_icns= Icn.objects.filter(program__in=program).order_by('-id')
    if query:
        qs1 = all_icns.filter(title__icontains=query)
        qs2 = all_icns.distinct().filter(program__title__icontains=query)
        qs3 = all_icns.distinct().filter(icn_number__icontains=query)
        
        
        icns = qs1.union(qs2, qs3).order_by('id')
    else:
        icns = all_icns

    context = {'icns': icns, 'count': all_icns.count()}
    return render(request, 'partial/icn_list.html', context)










@login_required(login_url='login')
def iarea_list(request, id):
    return render(request, 'partial/iarea_list.html', {
        'iareas': IcnImplementationArea.objects.filter(icn_id=id),
    })

@login_required(login_url='login')
def icn_submit_approval_list(request, id):
   

    icnsubmitlist = IcnSubmit.objects.filter(icn_id=id, submission_status=2)[:10]
    context = {'icnsubmitlist':icnsubmitlist}
   
  
    return render(request, 'partial/submit_approval_list.html', context )

@login_required(login_url='login')
def current_submit_approval_list(request, id):
    
    icn = Icn.objects.get(pk=id)
    if IcnSubmit.objects.filter(icn_id=icn.id).exists():
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        context = {'icn':icn, 'icnsubmit':icnsubmit}
    else:
        context = {'icn':icn}
  
    
    return render(request, 'partial/submit_list.html', context)

def update_approval_status(id):
    icnsubmit = get_object_or_404(IcnSubmit, pk=id)
    icnsubmitapproval_t = get_object_or_404(IcnSubmitApproval_T, submit_id_id=id)
    icnsubmitapproval_m = get_object_or_404(IcnSubmitApproval_M, submit_id_id=id)
    icnsubmitapproval_p = get_object_or_404(IcnSubmitApproval_P, submit_id_id=id)
    icnsubmitapproval_f = get_object_or_404(IcnSubmitApproval_F, submit_id_id=id)
   
    approval_t = icnsubmitapproval_t.approval_status
    approval_t = int(approval_t)
    
    approval_m = icnsubmitapproval_m.approval_status
    approval_m = int(approval_m)
   
    approval_f = icnsubmitapproval_f.approval_status
    approval_f = int(approval_f)
    
    
    if approval_t == 4 or  approval_m== 4  or approval_f== 4:
        Icn.objects.filter(pk=icnsubmit.icn_id).update(approval_status="Rejected")
    elif approval_t == 2 or approval_m == 2 or approval_f == 2:
        Icn.objects.filter(pk=icnsubmit.icn_id).update(approval_status="Revision Required")
    elif approval_t == 1 and approval_m == 1 and approval_f == 1:
        Icn.objects.filter(pk=icnsubmit.icn_id).update(approval_status="Pending Approval")
    elif approval_t == 3 and approval_m ==3 and approval_f==3:
         Icn.objects.filter(pk=icnsubmit.icn_id).update(approval_status="75% Approved")
    elif (approval_t == 3 and approval_m ==3 and approval_f !=3) or (approval_t == 3 and approval_m !=3 and approval_f ==3) or (approval_t != 3 and approval_m ==3 and approval_f ==3):
        Icn.objects.filter(pk=icnsubmit.icn_id).update(approval_status="50% Approved")
    elif (approval_t == 3 and approval_m !=3 and approval_f !=3) or (approval_t != 3 and approval_m ==3 and approval_f !=3) or (approval_t != 3 and approval_m !=3 and approval_f ==3):
        Icn.objects.filter(pk=icnsubmit.icn_id).update(approval_status="25% Approved") 
 
def update_approval_status_final(id):
    icnsubmit = get_object_or_404(IcnSubmit, pk=id)
    
    icnsubmitapproval_p = get_object_or_404(IcnSubmitApproval_P, submit_id_id=id)
    
   
    
    approval_p = icnsubmitapproval_p.approval_status
    approval_p = int(approval_p)
    
    if approval_p == 4 :
        Icn.objects.filter(pk=icnsubmit.icn_id).update(approval_status="Rejected")
    elif approval_p == 2:
        Icn.objects.filter(pk=icnsubmit.icn_id).update(approval_status="Revision Required")
    
    elif approval_p == 3:
        Icn.objects.filter(pk=icnsubmit.icn_id).update(approval_status="100% Approved")
   
   
   
    

@login_required(login_url='login')   
def add_impact(request, id):
    icn = get_object_or_404(Icn, pk=id)
    
    program = get_object_or_404(Program, pk=icn.program_id)
    
    if request.method == "POST":
        form = ImpactForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.icn = get_object_or_404(Icn, pk=id)
            selected_indicators = request.POST.getlist("indicators")
            items = Indicator.objects.filter(id__in=selected_indicators)
            instance.save()
            instance.indicators.add(*items)
            icn = get_object_or_404(Icn,id=id)
            if Impact.objects.filter(icn=icn).count() == 0 or Impact.objects.filter(icn=icn).count() == 1:
                return HttpResponseClientRedirect('/conceptnote/intervention/'+str(icn.id)+'/impact/')
            else:
                return HttpResponse(
                        status=204,
                        headers={
                            'HX-Trigger': json.dumps({
                            "ImpactListChanged": None,
                            "showMessage": f"{instance.icn} added."
                         })
                         })
    else:
        iform = ImpactForm(program=program)
    return render(request, 'partial/impact_form.html', {
        'iform': iform,
    })

@login_required(login_url='login')
def impact_list(request, id):
       
    impacts = Impact.objects.filter(icn_id=id)
    
    context = {'impacts': impacts}

    return render(request, 'partial/impact_list.html', context)

@login_required(login_url='login')
def icn_edit_impact(request, pk):
    impact = get_object_or_404(Impact, pk=pk)
    icn = get_object_or_404(Icn, pk=impact.icn_id)
    program = get_object_or_404(Program, pk=icn.program_id)
   
    if request.method == "POST":
        impact = Impact.objects.get(pk=pk)
        form = ImpactForm(request.POST, instance=impact)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ImpactListChanged": None,
                        "showMessage": f"{instance.pk} updated."
                    })
                })
        else:
            form = ImpactForm(request.POST, instance=impact)
            return render(request, 'partial/impact_form_edit.html', {
                'form': form,
                'impact': impact,
            })
    form = ImpactForm(instance=impact, program=program)
    return render(request, 'partial/impact_form_edit.html', {
        'form': form,
        'impact': impact,
    })


@login_required(login_url='login') 
def add_disaggregate(request, id):
    impact = Impact.objects.get(pk=id)
    form = DisaggregateForm(impact=impact)
    if request.method == 'POST':
        form = DisaggregateForm(request.POST, impact=impact)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.impact = impact
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ImpactListChanged": None,
                        "showMessage": f"{instance.pk} updated."
                    })
                })
        else:
            form = DisaggregateForm(request.POST, impact=impact)
            context = {'form':form, 'impact':impact}
            return render(request, 'partial/disaggregate_form.html', context)     
       
    context = {'form':form, 'impact':impact}
    return render(request, 'partial/disaggregate_form.html', context)

@login_required(login_url='login')
def edit_disaggregate(request, pk):
    disaggregate = get_object_or_404(Disaggregate, pk=pk)
    impact = get_object_or_404(Impact, pk=disaggregate.impact_id)
    if request.method == "POST":
        disaggregate = Disaggregate.objects.get(pk=pk)
        form = DisaggregateForm(request.POST, instance=disaggregate)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ImpactListChanged": None,
                        "showMessage": f"{instance.pk} updated."
                    })
                })
        else:
            form = DisaggregateForm(request.POST, instance=disaggregate)
            return render(request, 'partial/disaggregate_forme.html', {
                'form': form,
                'disaggregate': disaggregate,
                'impact': impact,
            })
    form = DisaggregateForm(instance=disaggregate)
    return render(request, 'partial/disaggregate_forme.html', {
        'form': form,
        'disaggregate': disaggregate,
        'impact':impact,
    })

@login_required(login_url='login') 
def delete_disaggregate(request, pk):
    disaggregate = get_object_or_404(Disaggregate, pk=pk)
    instance = disaggregate
    disaggregate.delete()
    return HttpResponse(
         status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ImpactListChanged": None,
                        "showMessage": f"{instance.pk} updated."
                    })
                })


@login_required(login_url='login')
def remove_impact(request, pk):
    
    impact = get_object_or_404(Impact, pk=pk)
    icn_id = impact.icn_id
    impact.delete()
    icn = get_object_or_404(Icn,id=icn_id)
   
    if Impact.objects.filter(icn=icn).count() != 0:
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                "ImpactListChanged": None,
                "showMessage": f"{impact.title} deleted."
              })
            })
    else:
        return HttpResponseClientRedirect('/conceptnote/intervention/'+str(icn.id)+'/impact/')
       
@login_required(login_url='login')
def download_env_att(request, id):
    document = get_object_or_404(Icn, id=id)
    response = HttpResponse(document.environmental_assessment_att, content_type='application/docx')
    response['Content-Disposition'] = f'attachment; filename="{document.environmental_assessment_att}"'
    return response

@login_required(login_url='login')
def icn_submit_form_partial(request, id): 
    icn = get_object_or_404(Icn, pk=id)
    if IcnSubmit.objects.filter(icn_id=icn.id).exists():
    
        
    
        form = IcnSubmitForm(user=request.user,icn=icn, sid=2)
    else:
        form = IcnSubmitForm(user=request.user,icn=icn,sid=2)
        
    context = {'form':form, 'icn':icn}
    return render(request, 'partial/partial_doc_form.html', context)

@login_required(login_url='login')    
def icn_submit_form_partialm(request, id): 
    icn = get_object_or_404(Icn, pk=id)
    
    
    form = IcnSubmitForm(user=request.user, did=2)
   
        
        
    context = {'form':form, 'icn':icn}
    return render(request, 'partial/partial_doc_form.html', context)

@login_required(login_url='login')    
def icn_approvalp_form_partial(request, id): 
    icn = get_object_or_404(Icn, pk=id)
    
    form = IcnApprovalPForm(user=request.user,icn=icn)
    
    context = {'form':form, 'icn':icn}
    return render(request, 'partial/partial_doc_form.html', context)

@login_required(login_url='login') 
def activities(request):
    user = request.user
    program = Program.objects.filter(users_role=user)
   
    icns = Icn.objects.filter(program__in=program).order_by('-id')
    activities = Activity.objects.filter(icn__in=icns).order_by('-id')
    context = {'activities':activities}
    
    return render(request, 'activities.html', context)

@login_required(login_url='login') 
def activity_detail(request, pk):
    
    context ={}
 
    # add the dictionary during initialization
  
    activity = Activity.objects.get(pk=pk)

    context = {'activity':activity}
    
    #icnsubmit= IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
    #icnsubmit = get_object_or_404(IcnSubmit, icn_id=icn.id).latest('id')


    return render(request, 'activity_step_profile_detail.html', context)

@login_required(login_url='login') 
def activity_add(request): 
    if request.method == "POST":
        form = ActivityForm(request.POST, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            selected_woredas = request.POST.getlist("aworeda")
            selected_co_agency = request.POST.getlist("alead_co_agency")
            items_woreda = ImplementationArea.objects.filter(id__in=selected_woredas)
            items_co_agency = Portfolio.objects.filter(id__in=selected_co_agency)
            instance.save()
            instance.aworeda.add(*items_woreda)
            instance.alead_co_agency.add(*items_co_agency)

            return redirect('activity_detail',instance.pk) 
        
        
        form = ActivityForm(request.POST, user=request.user)
        context = {'form':form}
        return render(request, 'activity_step_profile_add.html', context)
    
    form = ActivityForm(user=request.user)   
    context = {'form':form}
    return render(request, 'activity_step_profile_add.html', context)

@login_required(login_url='login')
def activity_edit(request, id): 
    activity = Activity.objects.get(pk=id)
    
    if request.method == "POST":
       
        form = ActivityForm(request.POST, instance=activity, user=request.user)
        if form.is_valid():
            instance = form.save()
            return redirect('activity_detail',instance.pk) 
        else:
            form = ActivityForm(request.POST,  instance=activity, user=request.user) 
            context = {'form':form, 'activity':activity}
            return render(request, 'activity_step_profile_edit.html', context)
            
    
    if activity.user == request.user and activity.status == False:
        form = ActivityForm(instance=activity,  user=request.user) 
        context = {'form':form, 'activity':activity}
        return render(request, 'activity_step_profile_edit.html', context)
    return HttpResponseRedirect(request.path_info)
    
@login_required(login_url='login')
def aregion(request, id):
    #icn = get_object_or_404(IcnImplementationArea, pk=id)
    if request.method == "POST":
        form = ActivityAreaFormE(request.POST or none)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.activity = Activity.objects.get(pk=id)
           
            instance.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "AareaListChanged": None,
                        "showMessage": f"{instance.woreda} added."
                    })
                })
        form = ActivityAreaFormE(request.POST)
        context = {'form': form}
    
        return render(request, 'aarea_form.html', context)
    
    form = ActivityAreaFormE()
    context = {'form': form}
    
    return render(request, 'aarea_form.html', context)

@login_required(login_url='login')
def aarea_list(request, id):
    return render(request, 'partial/aarea_list.html', {
        'aareas': ActivityImplementationArea.objects.filter(activity_id=id),
    })

@login_required(login_url='login') 
def activity_step_impact(request, id):
     activity = Activity.objects.get(id=id)
     
     impacts= ActivityImpact.objects.filter(activity_id=id)
     context = {'activity':activity, 'impacts': impacts}
     return render(request, 'activity_step_impact.html', context) 

@login_required(login_url='login')
def aarea_edit_form(request, pk):
    aarea = get_object_or_404(ActivityImplementationArea, pk=pk)
    activity = aarea.activity
    
    if request.method == "GET":
        aarea = get_object_or_404(ActivityImplementationArea, pk=int(pk))
        form = ActivityAreaFormE(instance=aarea)
        context = {'aarea': aarea, 'form': form }
        return render(request, 'aarea_edit_form.html', context)


    elif request.method == "PUT":
        aarea = get_object_or_404(ActivityImplementationArea, pk=int(pk))
        data = QueryDict(request.body).dict()
        form = ActivityAreaFormE(data, instance=aarea)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "AareaListChanged": None,
                        "showMessage": f"{instance.woreda} updated."
                    })
                }
            )
@login_required(login_url='login')        
def add_activity_impact(request, id):
    activity = get_object_or_404(Activity, pk=id)
    icn = get_object_or_404(Icn, pk=activity.icn_id)
    
    if request.method == "POST":
        form = ActivityImpactForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.activity = get_object_or_404(Activity, pk=id)
            selected_impact = request.POST.getlist("impact")
            items = Impact.objects.filter(id__in=selected_impact)
            instance.save()
            instance.impact.add(*items)
            
            activity = get_object_or_404(Activity,id=instance.activity_id)
   
            if ActivityImpact.objects.filter(activity_id=activity.id).count() == 1 or ActivityImpact.objects.filter(activity_id=activity.id).count() == 0:
                return HttpResponseClientRedirect('/conceptnote/activity/'+str(activity.id)+'/impact/')
            else:
                return HttpResponse(
                        status=204,
                        headers={
                            'HX-Trigger': json.dumps({
                            "AImpactListChanged": None,
                            "showMessage": f"{instance.title} added."
                        })
                        })
              
    else:
        form = ActivityImpactForm(icn=icn)
    return render(request, 'partial/activity_impact_form.html', {
        'form': form,
    })

@login_required(login_url='login')   
def activity_impact_list(request, id):
    return render(request, 'partial/activity_impact_list.html', {
        'activity_impacts': ActivityImpact.objects.filter(activity_id=id),
    })

@login_required(login_url='login')
def edit_activity_impact(request, pk):
    activity_impact = get_object_or_404(ActivityImpact, pk=pk)
    activity = get_object_or_404(Activity, pk=activity_impact.activity_id)
    icn = get_object_or_404(Icn, pk=activity.icn_id)
   
    if request.method == "POST":
        activity_impact = ActivityImpact.objects.get(pk=pk)
        form = ActivityImpactForm(request.POST, instance=activity_impact)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "AImpactListChanged": None,
                        "showMessage": f"{instance.pk} updated."
                    })
                })
    else:
        form = ActivityImpactForm(instance=activity_impact, icn=icn)
    return render(request, 'partial/activity_impact_form_edit.html', {
        'form': form,
        'activity_impact': activity_impact,
    })

@login_required(login_url='login')
def remove_activity_impact(request, pk):
    activity_impact = get_object_or_404(ActivityImpact, pk=pk)
    activity_id = activity_impact.activity_id
    activity_impact.delete()
    activity = get_object_or_404(Activity,id=activity_id)
   
    if ActivityImpact.objects.filter(activity=activity).count() != 0:
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                "AImpactListChanged": None,
                "showMessage": f"{activity_impact.title} deleted."
              })
            })
    else:
        return HttpResponseClientRedirect('/conceptnote/activity/'+str(activity.id)+'/impact/')
       
   
@login_required(login_url='login')
def adelete_area(request, pk):
    area = get_object_or_404(ActivityImplementationArea, pk=pk)
    activity = area.activity_id
    area.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "AareaListChanged": None,
                "showMessage": f"{area.woreda} deleted."
            })
        })
@login_required(login_url='login')
def search_results_view2(request):
    user = request.user
    if user.is_superuser:
        all_activities = Activity.objects.all()
    else:
        program = Program.objects.filter(users_role=user)
        icns = Icn.objects.filter(program__in=program).order_by('-id')
        all_activities = Activity.objects.filter(icn__in=icns).order_by('-id')
      

    query = request.GET.get('search', '')
    

   
    if query:
        qs1 = all_activities.filter(title__icontains=query)
        qs2 = all_activities.distinct().filter(icn__title__icontains=query)
        qs5 = all_activities.distinct().filter(icn__icn_number__icontains=query)
        qs4 = all_activities.distinct().filter(acn_number__icontains=query)
        qs3 = all_activities.distinct().filter(icn__program__title__icontains=query)
        activities = qs1.union(qs2, qs3, qs4, qs5).order_by('id')
       
    else:
        activities = all_activities

    context = {'activities': activities, 'count': activities.count()}
    return render(request, 'partial/activity_list.html', context)

@login_required(login_url='login')
def activity_submit_approval(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    context ={}
 
    # add the dictionary during initialization
    activity = Activity.objects.get(pk=pk)
    if ActivitySubmit.objects.filter(activity_id=activity.id).exists():
        activitysubmit = ActivitySubmit.objects.filter(activity_id=activity.id).latest('id')
        context = {'activity':activity, 'activitysubmit':activitysubmit}
    else:
        context = {'activity':activity}
    

    return render(request, 'activity_submit_approval.html', context)

@login_required(login_url='login') 
def current_activity_submit_approval_list(request, id):
    context ={}
 
    # add the dictionary during initialization
  
    activity = Activity.objects.get(pk=id)
    if ActivitySubmit.objects.filter(activity_id=activity.id).exists():
        activitysubmit = ActivitySubmit.objects.filter(activity_id=activity.id).latest('id')
        context = {'activity':activity, 'activitysubmit':activitysubmit}
    else:
        context = {'activity':activity}

    return render(request, 'partial/activity_submit_list.html', context)

@login_required(login_url='login')
def activity_submit_form(request, id, sid): 
    activity = get_object_or_404(Activity, pk=id)
    
    
    form = ActivitySubmitForm(activity=activity.id, sid=sid, user=request.user)
    
    if request.method == "POST":
        form = ActivitySubmitForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.activity = activity
            
            instance.user = request.user
            instance.save()
            #document = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
            #document_i = Document.objects.filter(icn=instance.icn, user=icn.user).count()+1
            
            activitysubmit = get_object_or_404(ActivitySubmit, pk=instance.pk)
            #Document.objects.create(user = icn.user, document = instance.document,  icn=instance.icn, description = document_i)
            if activitysubmit.submission_status_id == 2:
                Activity.objects.filter(pk=id).update(status=True)
                Activity.objects.filter(pk=id).update(approval_status="Pending Approval")
                ActivitySubmitApproval_T.objects.create(user = activity.technical_lead,submit_id = instance, document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                ActivitySubmitApproval_M.objects.create(user = activity.mel_lead,submit_id = instance, document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                ActivitySubmitApproval_P.objects.create(user = activity.program_lead,submit_id = instance,document = instance.document, approval_status=Approvalf_Status.objects.get(id=1))
                ActivitySubmitApproval_F.objects.create(user = activity.finance_lead,submit_id = instance,document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))

                send_activity_notify(activity.id, 12, instance.document_id)
               
                return HttpResponse(
                        status=204,
                        headers={
                            'HX-Trigger': json.dumps({
                            "SubmitApprovalListChanged": None,
                            "showMessage": f"{instance.id} added."
                         })
                         })
            
            elif activitysubmit.submission_status_id == 1:
                Activity.objects.filter(pk=id).update(status=False)
                Activity.objects.filter(pk=id).update(approval_status="Pending Submission")
                send_activity_notify(activity.id, 11, instance.document_id)
                              
                return HttpResponse(
                        status=204,
                        headers={
                            'HX-Trigger': json.dumps({
                            "SubmitApprovalListChanged": None,
                            "showMessage": f"{instance.id} added."
                         })
                         })
                 
        form = ActivitySubmitForm(request.POST,user=request.user,activity=activity, sid=sid)
        context = {'form':form, 'activity':activity, 'sid':sid}
        return render(request, 'activity_submit_form.html', context)
      
    context = {'form':form, 'activity':activity, 'sid':sid}
    return render(request, 'activity_submit_form.html', context)


@login_required(login_url='login') 
def activity_submit_document(request, id):
    context ={}
    activity = get_object_or_404(Activity, pk=id)
    dform = ActivityDocumentForm()
 
    if ActivityDocument.objects.filter(activity=activity.id).exists():
        major = ActivityDocument.objects.filter(activity=activity.id, user=activity.user).count() 
        last_initiator_doc = ActivityDocument.objects.filter(activity=activity.id, user=activity.user).latest('id') 
    
        minor = ActivityDocument.objects.filter(activity=activity.id, id__gt=last_initiator_doc.id).exclude(user=activity.user)
        minor = minor.count()
    else:
        major = 0
        minor = 0

    context = {'dform':dform}
    if request.method == 'POST':
        dform = ActivityDocumentForm(request.POST, request.FILES)
        if dform.is_valid():
            instance = dform.save(commit=False)
            instance.activity = activity
            instance.user = request.user
            if instance.user == activity.user:
                 major = major + 1
                 minor = 0
            else:
                 major = major 
                 minor = minor + 1
              
            instance.ver = "%s%s%s" %(major,'.',minor)

            instance.save()
            
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "DocListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        else:
            dform = ActivityDocumentForm(request.POST, request.FILES)
            context = {'dform':dform}
            return render(request, 'partial/activity_document_form.html', context)
                
    context = {'dform':dform}
    return render(request, 'partial/activity_document_form.html', context)
           
@login_required(login_url='login')            
def activity_submit_form_partial(request, id): 
    activity = get_object_or_404(Activity, pk=id)

    
    form = ActivitySubmitForm(user=request.user,activity=activity.id, sid=2)
    
    context = {'form':form, 'activity':activity}
    return render(request, 'partial/activity_partial_doc_form.html', context)

@login_required(login_url='login')
def activity_document_list(request, id):
    documents = ActivityDocument.objects.filter(activity_id=id)
    context = {'documents':documents}
           
          
    
    return render(request,'partial/activity_document_list.html', context)

@login_required(login_url='login')
def activity_submit_approval_list(request, id):
    activity_submit_list = ActivitySubmit.objects.filter(activity_id = id, submission_status=2)
    
    context = {'activity_submit_list': activity_submit_list }
    return render(request, 'partial/activity_submit_approval_list.html', context )

@login_required(login_url='login')
def activity_approvalt(request, id, did):
     
    activitysubmitApproval_t = get_object_or_404(ActivitySubmitApproval_T, submit_id_id=id)
    activitysubmit = get_object_or_404(ActivitySubmit, pk=id)
    
    activity =  get_object_or_404(Activity, id=activitysubmit.activity_id)

    if request.method == "GET":
        form = ActivityApprovalTForm(instance=activitysubmitApproval_t, activity=activity.id, did=did)
           
        context = {'activitysubmitapproval_t':activitysubmitApproval_t, 'form': form, 'activity':activity, 'did':did }
        return render(request, 'activity_approval_tform.html', context)
    
    elif request.method == "PUT":
        activitysubmitApproval_t = get_object_or_404(ActivitySubmitApproval_T, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = ActivityApprovalTForm(data, instance=activitysubmitApproval_t)
        if form.is_valid():
            instance =form.save()
           
            activitysubmit = get_object_or_404(ActivitySubmit, pk=id)
            activity =  get_object_or_404(Activity, id=activitysubmit.activity_id)
            update_activity_approval_status(activitysubmit.id)
            send_activity_notify(activity.id, 2, instance.document_id)
                            
                
            return HttpResponse(
                        status=204,
                        headers={
                            'HX-Trigger': json.dumps({
                            "SubmitApprovalListChanged": None,
                            "showMessage": f"{instance.id} added."
                         })
                         })
        
        return render(request, 'activity_approval_tform.html', {'form':form, 'did':did})

@login_required(login_url='login')
def activity_approvalm(request, id, did):
     
    activitysubmitApproval_m = get_object_or_404(ActivitySubmitApproval_M, submit_id_id=id)
    activitysubmit = get_object_or_404(ActivitySubmit, pk=id)
    
    activity =  get_object_or_404(Activity, id=activitysubmit.activity_id)

    if request.method == "GET":
        form = ActivityApprovalMForm(instance=activitysubmitApproval_m, activity=activity.id, did=did)
              
        context = {'activitysubmitapproval_m':activitysubmitApproval_m, 'form': form, 'activity':activity, 'did':did }
        return render(request, 'activity_approval_mform.html', context)
    
    elif request.method == "PUT":
        activitysubmitApproval_m = get_object_or_404(ActivitySubmitApproval_M, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = ActivityApprovalMForm(data, instance=activitysubmitApproval_m)
        if form.is_valid():
            instance =form.save()
           
            activitysubmit = get_object_or_404(ActivitySubmit, pk=id)
            activity =  get_object_or_404(Activity, id=activitysubmit.activity_id)
            update_activity_approval_status(activitysubmit.id)
            send_activity_notify(activity.id, 3,instance.document_id)
            
            return HttpResponse(
                        status=204,
                        headers={
                            'HX-Trigger': json.dumps({
                            "SubmitApprovalListChanged": None,
                            "showMessage": f"{instance.id} added."
                         })
                         })
        
        return render(request, 'activity_approval_mform.html', {'form':form, 'did':did})


@login_required(login_url='login')
def activity_approvalp(request, id, did):
     
    activitysubmitApproval_p = get_object_or_404(ActivitySubmitApproval_P, submit_id_id=id)
    activitysubmit = get_object_or_404(ActivitySubmit, pk=id)
    
    activity =  get_object_or_404(Activity, id=activitysubmit.activity_id)

    if request.method == "GET":
        form = ActivityApprovalPForm(instance=activitysubmitApproval_p, activity=activity.id, did=did)
              
        context = {'activitysubmitapproval_p':activitysubmitApproval_p, 'form': form, 'activity':activity, 'did':did }
        return render(request, 'activity_approval_pform.html', context)
    
    elif request.method == "PUT":
        activitysubmitApproval_p = get_object_or_404(ActivitySubmitApproval_P, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = ActivityApprovalPForm(data, instance=activitysubmitApproval_p, did=did)
        if form.is_valid():
            instance =form.save()
           
            activitysubmit = get_object_or_404(ActivitySubmit, pk=id)
            activity =  get_object_or_404(Activity, id=activitysubmit.activity_id)
            update_activity_approval_status_final(activitysubmit.id)
            send_activity_notify(activity.id, 5, instance.document_id)         
          
            return HttpResponse(
                        status=204,
                        headers={
                            'HX-Trigger': json.dumps({
                            "SubmitApprovalListChanged": None,
                            "showMessage": f"{instance.id} added."
                         })
                         })
    activitysubmitApproval_p = get_object_or_404(ActivitySubmitApproval_P, submit_id_id=id)
    data = QueryDict(request.body).dict()
    form = ActivityApprovalPForm(data, instance=activitysubmitApproval_p, did=did)
    return render(request, 'activity_approval_pform.html',  context = {'activitysubmitapproval_p':activitysubmitApproval_p, 'form': form, 'activity':activity, 'did':did })

@login_required(login_url='login') 
def activity_approvalf(request, id, did):
     
    activitysubmitApproval_f = get_object_or_404(ActivitySubmitApproval_F, submit_id_id=id)
    activitysubmit = get_object_or_404(ActivitySubmit, pk=id)
    
    activity =  get_object_or_404(Activity, id=activitysubmit.activity_id)

    if request.method == "GET":
        form = ActivityApprovalFForm(instance=activitysubmitApproval_f, activity=activity.id, did=did)     
        context = {'activitysubmitapproval_f':activitysubmitApproval_f, 'form': form, 'activity':activity,'did':did }
        return render(request, 'activity_approval_fform.html', context)
    
    elif request.method == "PUT":
        activitysubmitApproval_f = get_object_or_404(ActivitySubmitApproval_F, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = ActivityApprovalFForm(data, instance=activitysubmitApproval_f)
        if form.is_valid():
            instance =form.save()
            
            activitysubmit = get_object_or_404(ActivitySubmit, pk=id)
            activity =  get_object_or_404(Activity, id=activitysubmit.activity_id)
            update_activity_approval_status(activitysubmit.id)
            send_activity_notify(activity.id, 4, instance.document_id)
           
            return HttpResponse(
                        status=204,
                        headers={
                            'HX-Trigger': json.dumps({
                            "SubmitApprovalListChanged": None,
                            "showMessage": f"{instance.id} added."
                         })
                         })
        
        return render(request, 'activity_approval_fform.html', {'form':form, 'did':did, 'activity':activity })

def update_activity_approval_status(id):
    activitysubmit = get_object_or_404(ActivitySubmit, pk=id)
    activitysubmitapproval_t = get_object_or_404(ActivitySubmitApproval_T, submit_id_id=id)
    activitysubmitapproval_m = get_object_or_404(ActivitySubmitApproval_M, submit_id_id=id)
    activitysubmitapproval_f = get_object_or_404(ActivitySubmitApproval_F, submit_id_id=id)
    
    approval_t = activitysubmitapproval_t.approval_status
    approval_t = int(approval_t)
    approval_m = activitysubmitapproval_m.approval_status
    approval_m = int(approval_m)
    approval_f = activitysubmitapproval_f.approval_status
    approval_f = int(approval_f)
    
 
    
    if approval_t == 4 or approval_m== 4 or approval_f== 4:
        Activity.objects.filter(pk=activitysubmit.activity_id).update(approval_status="Rejected")
    elif approval_t == 2 or approval_m == 2 or approval_f == 2:
        Activity.objects.filter(pk=activitysubmit.activity_id).update(approval_status="Revision Required")
    elif approval_t == 1 and approval_m == 1 and approval_f == 1:
        Activity.objects.filter(pk=activitysubmit.activity_id).update(approval_status="Pending Approval")
    
    elif approval_t == 3 and approval_m ==3 and approval_f==3:
        Activity.objects.filter(pk=activitysubmit.activity_id).update(approval_status="75% Approved")
    elif (approval_t == 3 and approval_m ==3 and approval_f !=3) or (approval_t == 3 and approval_m !=3 and approval_f ==3) or (approval_t != 3 and approval_m ==3 and approval_f ==3):
        Activity.objects.filter(pk=activitysubmit.activity_id).update(approval_status="50% Approved")
    elif (approval_t == 3 and approval_m !=3 and approval_f !=3) or (approval_t != 3 and approval_m ==3 and approval_f !=3) or (approval_t != 3 and approval_m !=3 and approval_f ==3):
        Activity.objects.filter(pk=activitysubmit.activity_id).update(approval_status="25% Approved") 

def update_activity_approval_status_final(id):
    activitysubmit = get_object_or_404(ActivitySubmit, pk=id)
    activitysubmitapproval_p = get_object_or_404(ActivitySubmitApproval_P, submit_id_id=id)
    
    
    approval_p = activitysubmitapproval_p.approval_status
    approval_p = int(approval_p)
    
 
    
    if approval_p == 4:
        Activity.objects.filter(pk=activitysubmit.activity_id).update(approval_status="Rejected")
    elif approval_p == 2:
        Activity.objects.filter(pk=activitysubmit.activity_id).update(approval_status="Revision Required")
    elif approval_p == 3:
        Activity.objects.filter(pk=activitysubmit.activity_id).update(approval_status="100% Approved")
        
    
@login_required(login_url='login')
def downloada(request, id):
    document = get_object_or_404(ActivityDocument, id=id)
   
    response = HttpResponse(document.document, content_type='application/docx')
    response['Content-Disposition'] = f'attachment; filename="{document.document}"'
    return response









# Helper to build the needed formset

@login_required(login_url='login')
def add_impact_form(request):
    impact_form = ImpactForm()
    return render(request, 'partial/impact_form.html', {
        'impact_form': impact_form,
    })

@login_required(login_url='login')
def icn_approval_invoice(request, id):
    context ={}
 
    # add the dictionary during initialization
  
    icn = Icn.objects.get(pk=id)
    if IcnSubmit.objects.filter(icn_id=icn.id).exists():
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        context = {'icn':icn, 'icnsubmit':icnsubmit}
    else:
        context = {'icn':icn}

    return render(request, 'icn_approval_invoice.html', context)

@login_required(login_url='login')
def activity_approval_invoice(request, id):
    context ={}
 
    # add the dictionary during initialization
  
    activity = Activity.objects.get(pk=id)
    if ActivitySubmit.objects.filter(activity_id=activity.id).exists():
        activitysubmit = ActivitySubmit.objects.filter(activity_id=activity.id).latest('id')
        context = {'activity':activity, 'activitysubmit':activitysubmit}
    else:
        context = {'activity':activity}

    return render(request, 'activity_approval_invoice.html', context)

def program_lead(request):
    form = IcnForm(request.GET, user=request.user)
    return HttpResponse(form['program_lead'])

#gfdsfdsf ss
def program_changes(request):
    
    
    return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "programchanges": None,
                       
                    })
                })
@login_required(login_url='login')
def intervention_step(request, id):
   
 
    # add the dictionary during initialization
    icn = Icn.objects.get(pk=id)
    
    context = {'icn':icn}
    return render(request, 'intervention_step.html', context)

@login_required(login_url='login')
def icn_detail_modal(request, id):
    icn = Icn.objects.get(id=id)
    context = {'icn':icn}
    return render(request, 'partial/icn_detail_modal.html', context)

@login_required(login_url='login')
def icn_info(request):
    
    
    query = request.GET.get('icn', '')
    if query:
        
        icn = Icn.objects.get(id=query)
        
        return render(request, 'partial/intervention_info.html', {'icn':icn})
    
    return render(request, 'partial/intervention_info.html')

def iworedas(request):
    
    form = IcnForm(request.GET)
    return HttpResponse(form['iworeda'])


def send_activity_notify(id, uid, doc):
    activitydoc = ActivityDocument.objects.get(id=doc)
    f = activitydoc.document
    f.open()
# msg.attach(filename, content, mimetype)
    
    activity = get_object_or_404(Activity, id=id)
    if uid == 12:
        subject = 'Request for Activity Approval'
        initiator = activity.user.profile.full_name
        user_role = 'Initiator'
    elif uid == 11:
        subject = 'Activity Approval Request temporarily withdrawn'
        initiator = activity.user.profile.full_name
        user_role = 'Initiator'
        
    elif uid ==2:
        subject = 'Activity Approval Status changed'
        initiator = activity.technical_lead.user.profile.full_name
        user_role = 'Technical Lead'
    elif uid ==3:
        subject = 'Activity Approval Status changed'
        initiator = activity.mel_lead.user.profile.full_name
        user_role = 'MEL Lead'
    elif uid ==4:
        subject = 'Activity Approval Status changed'
        initiator = activity.finance_lead.user.profile.full_name
        user_role = 'Finance Lead'
    elif uid ==5:
        subject = 'Activity Final Approval Status changed'
        initiator = activity.program_lead.user.profile.full_name
        user_role = 'Program Lead'
        

    subject = subject
    context = {
                "program": activity.icn.program,
                "title": activity.title,
                "id": activity.id,
                "cn_id": activity.acn_number,
                "creator": activity.user.profile.full_name,
                "initiator": initiator,
                "user_role": user_role,
            
                
                }
    html_message = render_to_string("partial/activity_mail.html", context=context)
    plain_message = strip_tags(html_message)
    recipient_list = [activity.user.email, activity.technical_lead.user.email, activity.mel_lead.user.email,  activity.finance_lead.user.email]
        
    message = EmailMultiAlternatives(
        subject = subject, 
        body = plain_message,
        from_email = 'Mercy Corps CNMS',
        to= recipient_list
            )
    
    message.attach_alternative(html_message, "text/html")
   
    message.attach(basename(f.name), f.read(), guess_type(f.name)[0])
    f.close()
    message.send()
    
    if uid !=5 and activity.approval_status == '75% Approved':
        subject = 'Request for Activity Final Approval'
        html_message = render_to_string("partial/activity_mail.html", context=context)
        plain_message = strip_tags(html_message)
        recipient_list = [activity.user.email, activity.mel_lead.user.email, activity.technical_lead.user.email, activity.program_lead.user.email, activity.finance_lead.user.email]
        
        message = EmailMultiAlternatives(
            subject = subject, 
            body = plain_message,
            from_email = 'Mercy Corps CNMS',
            to= recipient_list
                )
        
        message.attach_alternative(html_message, "text/html")
        message.attach(basename(f.name), f.read(), guess_type(f.name)[0])
        f.close()
        message.send()

def send_icn_notify(id, uid, doc):
    icndoc = Document.objects.get(id=doc)
    f = icndoc.document
    f.open()
    icn = get_object_or_404(Icn, id=id)
    if uid == 12:
        subject = 'Request for Intervention Approval'
        initiator = icn.user.profile.full_name
        user_role = 'Initiator'
    elif uid == 11:
        subject = 'Intervention Approval Request temporarily withdrawn'
        initiator = icn.user.profile.full_name
        user_role = 'Initiator'
        
    elif uid ==2:
        subject = 'Intervention Approval Status changed'
        initiator = icn.technical_lead.user.profile.full_name
        user_role = 'Technical Lead'
    elif uid ==3:
        subject = 'Intervention Approval Status changed'
        initiator = icn.mel_lead.user.profile.full_name
        user_role = 'MEL Lead'
    elif uid ==4:
        subject = 'Intervention Approval Status changed'
        initiator = icn.finance_lead.user.profile.full_name
        user_role = 'Finance Lead'
    elif uid ==5:
        subject = 'Intervention Final Approval Status changed'
        initiator = icn.program_lead.user.profile.full_name
        user_role = 'Program Lead'
        

    subject = subject
    context = {
                "program": icn.program,
                "title": icn.title,
                "id": icn.id,
                "cn_id": icn.icn_number,
                "creator": icn.user.profile.full_name,
                "initiator": initiator,
                "user_role": user_role,
            
                
                }
    html_message = render_to_string("partial/intervention_mail.html", context=context)
    plain_message = strip_tags(html_message)
    recipient_list = [icn.user.email, icn.mel_lead.user.email, icn.technical_lead.user.email,  icn.finance_lead.user.email]
        
    message = EmailMultiAlternatives(
        subject = subject, 
        body = plain_message,
        from_email = 'Mercy Corps CNMS',
        to= recipient_list
            )
        
    message.attach_alternative(html_message, "text/html")
    message.attach(basename(f.name), f.read(), guess_type(f.name)[0])
    f.close()
    message.send()
    
    if uid !=5 and icn.approval_status == '75% Approved':
        subject = 'Request for Intervention Final Approval'
        html_message = render_to_string("partial/intervention_mail.html", context=context)
        plain_message = strip_tags(html_message)
        recipient_list = [icn.user.email, icn.technical_lead.user.email, icn.mel_lead.user.email ,icn.program_lead.user.email, icn.finance_lead.user.email]
        
        message = EmailMultiAlternatives(
            subject = subject, 
            body = plain_message,
            from_email = 'Mercy Corps CNMS',
            to= recipient_list
                )
        
        message.attach_alternative(html_message, "text/html")
        message.attach(basename(f.name), f.read(), guess_type(f.name)[0])
        f.close()
        message.send()