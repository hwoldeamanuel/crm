from django.shortcuts import render
from django.core.files.uploadedfile import TemporaryUploadedFile
import json
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse 
from django.http import QueryDict
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from .models import IcnReport, ActivityReport, ActivityReportImpact,ActivityReportImplementationArea,  IcnReportImplementationArea,  Impact, IcnReportSubmit, IcnReportDocument, IcnReportSubmitApproval_M,  IcnReportSubmitApproval_P, IcnReportSubmitApproval_F, IcnReportSubmitApproval_T, ActivityReportDocument, ActivityReportSubmit, ActivityReportSubmitApproval_F,ActivityReportSubmitApproval_P,ActivityReportSubmitApproval_T, IcnReportImpact, ActivityImpact, ActivityReportSubmitApproval_M
from .forms import IcnReportForm, ActivityReportForm,ActivityReportImpactForm, ActivityReportImpactForm, ActivityReportAreaFormE, IcnReportAreaFormE, IcnReportSubmitForm,  IcnReportDocumentForm, IcnReportApprovalMForm, IcnReportApprovalTForm, IcnReportApprovalFForm, IcnReportApprovalPForm, ActivityReportSubmitForm, ActivityReportDocumentForm, ActivityReportApprovalFForm, ActivityReportApprovalPForm,ActivityReportApprovalTForm,IcnReportImpactForm, ActivityReportApprovalMForm
from program.models import  Program
from django.http import QueryDict
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Max, Avg,Sum,Count
from conceptnote.models import Icn, Activity, IcnImplementationArea
from django.forms import formset_factory 
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.template import Context
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from render_block import render_block_to_string
from django_htmx.http import HttpResponseClientRedirect
from django_htmx.http import HttpResponseClientRedirect
from django_htmx.http import HttpResponseClientRefresh
from portfolio.models import Portfolio
from program.models import ImplementationArea, UserRoles
from app_admin.models import Approvalf_Status, Approvalt_Status, Submission_Status
# Create your views here.



@login_required(login_url='login') 
def icnreports(request):
    if IcnReport.objects.exists():
        reports = IcnReport.objects.all().order_by('-id')
        icns = Icn.objects.all().order_by('-id')
        context = {'reports':reports, 'icns':icns}
    else:
        icns = Icn.objects.all().order_by('-id')
        context = {'icns':icns}
    
    return render(request, 'report/reports.html', context)


@login_required(login_url='login') 
def icnreport_add(request, id): 
    icn = Icn.objects.get(pk=id)
   
    if request.method == "POST":
        form = IcnReportForm(request.POST,request.FILES, user=request.user, icn=icn.id)
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
                     
            return redirect('icnreport_detail',instance.icn_id) 
        
        form = IcnReportForm(request.POST,request.FILES, user=request.user, icn=icn.id)   
        context = {'form':form, 'icn':icn}
        return render(request, 'report/icnreport_step_profile_new.html', context)
    
   
    
    program = Program.objects.filter(id=icn.program_id)
    current_user = request.user
    program_users = UserRoles.objects.filter(program__in=program, is_pcn_initiator=True)
    if User.objects.filter(id=current_user.id,userroles__in=program_users).exists():
        form = IcnReportForm(user=request.user, icn=icn.id)   
        context = {'form':form, 'icn':icn}
        return render(request, 'report/icnreport_step_profile_new.html', context)
    return redirect('icn_step_approval',icn.id) 
    

           
        
    
   




@login_required(login_url='login')  
def icnreport_edit(request, id): 
    icn = Icn.objects.get(id=id)
    icnreport = IcnReport.objects.get(icn_id=icn.id)
   
    impacts = Impact.objects.filter(icn_id=id)
    
    if request.method == "POST":
       
        form = IcnReportForm(request.POST,request.FILES, instance=icnreport, icn=icn.id,user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
                       
            selected_woredas = request.POST.getlist("iworeda")
            
            items_woreda = ImplementationArea.objects.filter(id__in=selected_woredas)
           
            instance.save()
            instance.iworeda.add(*items_woreda)
           
                     
            return redirect('icnreport_detail',instance.icn_id)
            
            
            
        
        form = IcnReportForm(request.POST, request.FILES, instance=icnreport, user=request.user, icn=icn) 
        context = {'form':form, 'icn':icn, 'icnreport':icnreport}
        return render(request, 'report/icnreport_step_profile_new.html', context)
            
    icn = Icn.objects.get(pk=id)
    program = Program.objects.filter(id=icn.program_id)
    current_user = request.user
    program_users = UserRoles.objects.filter(program__in=program, is_pcn_initiator=True)
    if User.objects.filter(id=current_user.id,userroles__in=program_users).exists():
        form = IcnReportForm(instance=icnreport, user=current_user, icn=icn.id)   
        context = {'form':form, 'icn':icn, 'user':current_user}
        return render(request, 'report/icnreport_step_profile_new.html', context)
    return redirect('icn_step_approval',icn.id) 
                



@login_required(login_url='login') 
def icnreport_detail(request, id):

    icn = Icn.objects.get(id=id)

    context ={}
 
    # add the dictionary during initialization
    if IcnReport.objects.filter(icn_id=icn.id).exists():
         
        icnreport = IcnReport.objects.get(icn_id=icn.id)
   
        if IcnReportSubmit.objects.filter(icnreport_id=icnreport.id).exists():
            icnreportsubmit = IcnReportSubmit.objects.filter(icnreport_id=icnreport.id).latest('id')
            context = {'icn':icn,'icnreport':icnreport, 'icnreportsubmit':icnreportsubmit}
        else:
            context = {'icn': icn, 'icnreport':icnreport}
        
        return render(request, 'report/icnreport_step_profile_detail.html', context)
    
    return redirect('icnreport_add',id=id) 
    
@login_required(login_url='login') 
def icnreport_step_impact(request, id):
    if Icn.objects.filter(id=id).exists():
        icn = Icn.objects.get(id=id)

        if icn.approval_status != '100% Approved':
            return redirect('icn_step_approval',id=icn.id) 
        
        elif IcnReport.objects.filter(icn_id=id).exists():
            icnreport = IcnReport.objects.filter(icn_id=id)
            impacts = Impact.objects.filter(icn_id=id)
            context = {'icn':icn, 'icnreport':icnreport, 'impacts': impacts}

            return render(request, 'report/icnreport_step_impact.html', context)
        else:
            
            return redirect('icnreport_add',id=icn.id)
    else:
        return redirect('icn_new') 
        
    
@login_required(login_url='login') 
def activityreport_step_impact(request, id):
    if Activity.objects.filter(id=id).exists():
        activity = Activity.objects.get(id=id)
    
        if  ActivityReport.objects.filter(activity_id=id).exists():
            activityreport = ActivityReport.objects.filter(activity_id=id)
            if ActivityImpact.objects.filter(activity_id=id).exists():
                impacts = ActivityImpact.objects.filter(activity_id=id)
                context = {'activity':activity, 'activityreport':activityreport, 'impacts': impacts}

                return render(request, 'report/activityreport_step_impact.html', context)
        else:
            return redirect('activityreport_add',id=activity.id)
        
    return redirect('activity_add')
            
        


 



@login_required(login_url='login') 
def icnreport_submit_form(request, id, sid): 
    icn = Icn.objects.get(id=id)
    icnreport = IcnReport.objects.get(icn_id=icn.id)
    form = IcnReportSubmitForm(sid=sid, icnreport=icnreport.id, user=request.user)       
    
    if request.method == "POST":
        form = IcnReportSubmitForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.icnreport = icnreport
            
            instance.user = request.user
            instance.save()
            #document = IcnReportSubmit.objects.filter(icnreport_id=icnreport.id).latest('id')
            #document_i = Document.objects.filter(icnreport=instance.icnreport, user=icnreport.user).count()+1
            
            icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=instance.pk)
            #Document.objects.create(user = icnreport.user, document = instance.document,  icnreport=instance.icnreport, description = document_i)
            if icnreportsubmit.submission_status_id == 2:
                IcnReport.objects.filter(icn_id=icn.id).update(status=True)
                IcnReport.objects.filter(icn_id=icn.id).update(approval_status="Pending Approval")
                IcnReportSubmitApproval_T.objects.create(user = icnreport.technical_lead,submit_id = instance, document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                IcnReportSubmitApproval_M.objects.create(user = icnreport.mel_lead,submit_id = instance, document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                IcnReportSubmitApproval_P.objects.create(user = icnreport.program_lead,submit_id = instance,document = instance.document, approval_status=Approvalf_Status.objects.get(id=1))
                IcnReportSubmitApproval_F.objects.create(user = icnreport.finance_lead,submit_id = instance,document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                
                send_icnreport_notify(icnreport.id, 12)
                
                return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
            elif icnreportsubmit.submission_status_id == 1:
                IcnReport.objects.filter(icn_id=icn.id).update(status=False)
                IcnReport.objects.filter(icn_id=icn.id).update(approval_status="Pending Submission")
                send_icnreport_notify(icnreport.id, 11)
                return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })

      
    context = {'form':form, 'icnreport':icnreport, 'sid':sid }
    return render(request, 'report/icnreport_submit_form copy.html', context)

@login_required(login_url='login') 
def icnreport_submit_detail(request, pk):
    
    context ={}
 
    # add the dictionary during initialization
  
    icnreportsubmit = IcnReportSubmit.objects.get(pk=pk,  submission_status=2)
    
   

    context = {'icnreportsubmit':icnreportsubmit}

    return render(request, 'report/icnreportsubmit_detail.html', context)


@login_required(login_url='login') 
def icnreport_approvalt(request, id, did):
     
    icnreportsubmitApproval_t = get_object_or_404(IcnReportSubmitApproval_T, submit_id_id=id)
    icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=id)
    
    icnreport =  get_object_or_404(IcnReport, id=icnreportsubmit.icnreport_id)
    
       
    if request.method == "GET":
        form = IcnReportApprovalTForm(instance=icnreportsubmitApproval_t, user=request.user, did=did, icnreport=icnreport.id)
        context = {'icnreportsubmitapproval_t':icnreportsubmitApproval_t, 'form': form, 'icnreport':icnreport, 'did':did}
        return render(request, 'report/icnreport_approval_tform.html', context)
    
    elif request.method == "PUT":
        icnreportsubmitApproval_t = get_object_or_404(IcnReportSubmitApproval_T, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = IcnReportApprovalTForm(data, instance=icnreportsubmitApproval_t, did=did)
        if form.is_valid():
            instance =form.save()
           
            icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=id)
            icnreport =  get_object_or_404(IcnReport, id=icnreportsubmit.icnreport_id)
            myid = int(icnreportsubmit.id)
            update_approval_status(myid)
            send_icnreport_notify(icnreport.id, 2) 
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'report/icnreport_approval_tform.html', {'form':form, 'did':did})
  
@login_required(login_url='login') 
def icnreport_approvalm(request, id, did):
     
    icnreportsubmitApproval_m = get_object_or_404(IcnReportSubmitApproval_M, submit_id_id=id)
    icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=id)
    
    icnreport =  get_object_or_404(IcnReport, id=icnreportsubmit.icnreport_id)
    
       
    if request.method == "GET":
        form = IcnReportApprovalMForm(instance=icnreportsubmitApproval_m, user=request.user, icnreport=icnreport.id,did=did)
        context = {'icnreportsubmitapproval_m':icnreportsubmitApproval_m, 'form': form, 'icnreport':icnreport, 'did':did}
        return render(request, 'report/icnreport_approval_mform.html', context)
    
    elif request.method == "PUT":
        icnreportsubmitApproval_m = get_object_or_404(IcnReportSubmitApproval_M, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = IcnReportApprovalMForm(data, instance=icnreportsubmitApproval_m, did=did)
        if form.is_valid():
            instance =form.save()
           
            icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=id)
            icnreport =  get_object_or_404(IcnReport, id=icnreportsubmit.icnreport_id)
            myid = int(icnreportsubmit.id)
            update_approval_status(myid)
            send_icnreport_notify(icnreport.id, 3)
           
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'report/icnreport_approval_mform.html', context)
    
@login_required(login_url='login') 
def icnreport_approvalp(request, id, did):
    
    icnreportsubmitApproval_p = get_object_or_404(IcnReportSubmitApproval_P, submit_id_id=id)
    icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=id)
    
    icnreport =  get_object_or_404(IcnReport, id=icnreportsubmit.icnreport_id)
    
       
    if request.method == "GET":
        form = IcnReportApprovalPForm(instance=icnreportsubmitApproval_p, user=request.user, icnreport=icnreport.id, did=did)         
        context = {'icnreportsubmitapproval_p':icnreportsubmitApproval_p, 'form': form, 'icnreport':icnreport, 'did':did}
        return render(request, 'report/icnreport_approval_pform.html', context)
    
    elif request.method == "PUT":
        icnreportsubmitApproval_p = get_object_or_404(IcnReportSubmitApproval_P, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = IcnReportApprovalPForm(data, instance=icnreportsubmitApproval_p, did=did)
        if form.is_valid():
            instance = form.save()
            icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=id)
            update_approval_status_final(icnreportsubmit.id)
            send_icnreport_notify(icnreport.id, 5)
           
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'report/icnreport_approval_pform.html', {'form':form, 'did':did})



@login_required(login_url='login') 
def icnreport_approvalf(request, id, did):
    icnreportsubmitApproval_f = get_object_or_404(IcnReportSubmitApproval_F, submit_id_id=id)
    icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=id)
    
    icnreport =  get_object_or_404(IcnReport, id=icnreportsubmit.icnreport_id)

       
    if request.method == "GET":
        form = IcnReportApprovalFForm(instance=icnreportsubmitApproval_f, user=request.user, icnreport=icnreport.id, did=did)
                   
        context = {'icnreportsubmitapproval_f':icnreportsubmitApproval_f, 'form': form, 'icnreport':icnreport, 'did':did}
        return render(request, 'report/icnreport_approval_fform.html', context)
    
    elif request.method == "PUT":
        icnreportsubmitApproval_f = get_object_or_404(IcnReportSubmitApproval_F, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = IcnReportApprovalFForm(data, instance=icnreportsubmitApproval_f, did=did)
        if form.is_valid():
            instance = form.save()
            icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=id)
            update_approval_status(icnreportsubmit.id)
            send_icnreport_notify(icnreport.id, 4)
           
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'report/icnreport_approval_fform.html', context)

@login_required(login_url='login') 
def icnreport_submit_approval(request, id):
    icn = Icn.objects.get(id=id)
    
 
    # add the dictionary during initialization
    icnreport = IcnReport.objects.get(icn_id=icn.id)
    if IcnReportSubmit.objects.filter(icnreport_id=icnreport.id).exists():
        icnreportsubmit = IcnReportSubmit.objects.filter(icnreport_id=icnreport.id).latest('id')
        context = {'icn':icn, 'icnreport':icnreport, 'icnreportsubmit':icnreportsubmit}
    else:
        context = {'icn':icn, 'icnreport':icnreport}
    

    return render(request, 'report/icnreport_step_approval.html', context)


@login_required(login_url='login') 
def icnreport_submit_list(request, id):
    context ={}
 
    # add the dictionary during initialization
    
    icnreport = IcnReport.objects.get(pk=id)
    if IcnReportSubmit.objects.filter(icnreport_id=icnreport.id).exists():
        icnsubmit = IcnReportSubmit.objects.filter(icnreport_id=icnreport.id).latest('id')
        context = {'icnreport':icnreport, 'icnsubmit':icnsubmit}
    else:
        context = {'icnreport':icnreport}

    return render(request, 'report/partial/submit_list.html', context)



@login_required(login_url='login')  
def icnreport_submit_document(request, id):
    context ={}
    icnreport = get_object_or_404(IcnReport, pk=id)
    dform = IcnReportDocumentForm()
    if IcnReportDocument.objects.filter(icnreport=icnreport.id).exists():
        major = IcnReportDocument.objects.filter(icnreport=icnreport.id, user=icnreport.user).count()
        last_initiator_doc = IcnReportDocument.objects.filter(icnreport=icnreport.id, user=icnreport.user).latest('id') 
        minor = IcnReportDocument.objects.filter(icnreport=icnreport.id, id__gt=last_initiator_doc.id).exclude(user=icnreport.user)
        minor = minor.count()
    else:
        major = 0
        minor = 0

    context = {'dform':dform}
    if request.method == 'POST':
        dform = IcnReportDocumentForm(request.POST, request.FILES)
        if dform.is_valid():
            instance = dform.save(commit=False)
            instance.icnreport = icnreport
            instance.user = request.user
            if instance.user == icnreport.user:
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
       dform = IcnReportDocumentForm()
       context = {'dform':dform}
       return render(request, 'report/partial/icnreport_document_form copy.html', context)
           
            
       
   

@login_required(login_url='login')        
def document_list(request, id):
    icn = Icn.objects.get(id=id)
    icnreport = IcnReport.objects.get(icn_id=icn.id)
    documents = IcnReportDocument.objects.filter(icnreport_id=icnreport.id)
    context = {'documents':documents}
           
          
    
    return render(request,'report/partial/icnreport_document_list.html', context)
       


@login_required(login_url='login') 
def download(request, id):
    document = get_object_or_404(IcnReportDocument, id=id)
    response = HttpResponse(document.document, content_type='application/docx')
    response['Content-Disposition'] = f'attachment; filename="{document.document}"'
    return response


@login_required(login_url='login') 
def icnreport_filter(request):
    query = request.GET.get('search', '')
    print(query)
    if query:
        qs1 = IcnReport.objects.filter(icn__title__icontains=query)
        qs2 = IcnReport.objects.distinct().filter(icn__program__title__icontains=query)
        
        
        icnreports = qs1.union(qs2).order_by('id')
    else:
        icnreports = IcnReport.objects.all()

    context = {'icnreports': icnreports, }
    return render(request, 'partial/icnreport_list.html', context)













@login_required(login_url='login') 
def submit_approval_list(request, id):
    icn = Icn.objects.get(id=id)
    icnreport = get_object_or_404(IcnReport,icn_id=icn.id)
    icnreport_submit_list = IcnReportSubmit.objects.filter(icnreport_id = icnreport.id, submission_status=2)
    
    context = {'icnreport_submit_list': icnreport_submit_list }
    return render(request, 'report/partial/icnreport_submit_approval_list.html', context )

@login_required(login_url='login') 
def current_submit_approval_list(request, id):
    icn = Icn.objects.get(id=id)
    if IcnReport.objects.filter(icn_id=icn.id).exists():
        icnreport = IcnReport.objects.get(icn_id=icn.id)
        if IcnReportSubmit.objects.filter(icnreport_id=icnreport.id).exists():
            icnreportsubmit = IcnReportSubmit.objects.filter(icnreport_id=icnreport.id).latest('id')
            context = {'icn':icn, 'icnreport':icnreport, 'icnreportsubmit':icnreportsubmit}
        else:
            context = {'icn':icn, 'icnreport':icnreport}
    else:
        context = {'icn':icn}
  
    
    return render(request, 'report/partial/icnreport_submit_list.html', context)



def update_approval_status(id):
    icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=id)
    icnsubmitapproval_t = get_object_or_404(IcnReportSubmitApproval_T, submit_id_id=id)
    icnsubmitapproval_m = get_object_or_404(IcnReportSubmitApproval_M, submit_id_id=id)
    icnsubmitapproval_f = get_object_or_404(IcnReportSubmitApproval_F, submit_id_id=id)
    
    approval_t = icnsubmitapproval_t.approval_status
    approval_t = int(approval_t)
    approval_m = icnsubmitapproval_m.approval_status
    approval_m = int(approval_m)
    approval_f = icnsubmitapproval_f.approval_status
    approval_f = int(approval_f)
        
    if approval_t == 4 or approval_m== 4 or approval_f== 4:
        IcnReport.objects.filter(pk=icnreportsubmit.icnreport_id).update(approval_status="Rejected")
    if approval_t == 2 or approval_m== 2 or approval_f== 2:
        IcnReport.objects.filter(pk=icnreportsubmit.icnreport_id).update(approval_status="Revision Required")
    elif approval_t == 1 and approval_m == 1 and approval_m == 1:
        IcnReport.objects.filter(pk=icnreportsubmit.icnreport_id).update(approval_status="Pending Approval")
    elif approval_t == 3 and approval_m ==3 and approval_f==3:
         IcnReport.objects.filter(pk=icnreportsubmit.icnreport_id).update(approval_status="75% Approved")
    elif (approval_t == 3 and approval_m ==3 and approval_f !=3) or (approval_t == 3 and approval_m !=3 and approval_f ==3) or (approval_t != 3 and approval_m ==3 and approval_f ==3):
        IcnReport.objects.filter(pk=icnreportsubmit.icnreport_id).update(approval_status="50% Approved")
    elif (approval_t == 3 and approval_m !=3 and approval_f !=3) or (approval_t != 3 and approval_m ==3 and approval_f !=3) or (approval_t != 3 and approval_m !=3 and approval_f ==3):
        IcnReport.objects.filter(pk=icnreportsubmit.icnreport_id).update(approval_status="25% Approved") 

      
def update_approval_status_final(id):
    icnreportsubmit = get_object_or_404(IcnReportSubmit, pk=id)
    icnsubmitapproval_p = get_object_or_404(IcnReportSubmitApproval_P, submit_id_id=id)
    
    
    approval_p = icnsubmitapproval_p.approval_status
    approval_p = int(approval_p)
    
    if approval_p == 4:
        IcnReport.objects.filter(pk=icnreportsubmit.icnreport_id).update(approval_status="Rejected")
    elif approval_p == 2:
        IcnReport.objects.filter(pk=icnreportsubmit.icnreport_id).update(approval_status="Revision Required")
    elif approval_p == 3:
        IcnReport.objects.filter(pk=icnreportsubmit.icnreport_id).update(approval_status="100% Approved")
                


@login_required(login_url='login')    
def add_icnreport_impact(request, id):
    impact = Impact.objects.get(pk=id)
    icn = Icn.objects.get(id=impact.icn_id)
    
    
    icnreport = IcnReport.objects.get(icn_id=icn.id)
    if request.method == "POST":
       
        form = IcnReportImpactForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.impact = impact
            instance.icnreport = icnreport
            instance.save()
            
            
            if IcnReportImpact.objects.filter(icnreport_id=instance.icnreport_id).count() == 1:
                return HttpResponseClientRedirect('/report/intervention/'+str(icn.id)+'/impact/')
            else:
                return HttpResponse(
           
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ImpactListChanged": None,
                        "showMessage": f"{instance.pk} updated."
                    })
                })
    else:
        form = IcnReportImpactForm()
    return render(request, 'report/partial/icnreport_impact_form.html', {
        'form': form,
        'impact': impact,
    })


@login_required(login_url='login') 
def icnreport_impact_list(request, id):
    impacts = Impact.objects.filter(icn_id=id)
    context = {'impacts':impacts}
    return render(request, 'report/partial/impact_list.html', context)



@login_required(login_url='login') 
def edit_impact(request, pk):
    impact = get_object_or_404(IcnReportImpact, pk=pk)
    icnreport = get_object_or_404(IcnReport, pk=impact.icnreport_id)
    
   
    if request.method == "POST":
        impact = IcnReportImpact.objects.get(pk=pk)
        form = IcnReportImpactForm(request.POST, instance=impact)
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
        form = IcnReportImpactForm(instance=impact)
    return render(request, 'report/partial/icnreport_impact_form_edit.html', {
        'form': form,
        'impact': impact,
    })


@login_required(login_url='login') 
def icnreport_remove_impact(request, pk):
    impact = get_object_or_404(Impact, pk=pk)
    impact.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "ImpactListChanged": None,
                "showMessage": f"{impact} deleted."
            })
        })




@login_required(login_url='login') 
def icnreport_submit_form_partial(request, id): 
    icnreport = get_object_or_404(IcnReport, pk=id)
    form = IcnReportSubmitForm(user=request.user,icnreport=icnreport, sid=2)
    
    context = {'form':form, 'icnreport':icnreport}
    return render(request, 'report/partial/icnreport_partial_doc_form.html', context)


@login_required(login_url='login')  
def activitiesreport(request):
    if ActivityReport.objects.exists():
        reports = ActivityReport.objects.all().order_by('-id')
        acns = Activity.objects.all().order_by('-id')
        context = {'reports':reports, 'acns':acns}
    else:
        acns = Activity.objects.all().order_by('-id')
        context = {'acns':acns}
    
    
    return render(request, 'report/activitiesreport.html', context)


@login_required(login_url='login') 
def activityreport_detail(request, id):
    activity = Activity.objects.get(id=id)

    context ={}

    # add the dictionary during initialization
    if ActivityReport.objects.filter(activity_id=activity.id).exists():
            
        activityreport = ActivityReport.objects.get(activity_id=activity.id)

        if ActivityReportSubmit.objects.filter(activityreport_id=activityreport.id).exists():
            activityreportsubmit = ActivityReportSubmit.objects.filter(activityreport_id=activityreport.id).latest('id')
            context = {'activity':activity,'activityreport':activityreport, 'activityreportsubmit':activityreportsubmit}
        else:
            context = {'activity': activity, 'activityreport':activityreport}
        
        return render(request, 'report/activityreport_step_profile_detail.html', context)

    return redirect('activityreport_add',id=id) 

@login_required(login_url='login')  
def activityreport_add(request, id): 
    activity = Activity.objects.get(id=id)
    activitympacts =  ActivityImpact.objects.filter(activity_id=id)
    if request.method == "POST":
        form = ActivityReportForm(request.POST,request.FILES, user=request.user, activity=activity.id)
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
            return redirect('activityreport_detail',id) 
              
        form = ActivityReportForm(request.POST,request.FILES, user=request.user, activity=activity.id)   
        context = {'form':form, 'activity':activity}
        return render(request, 'report/activityreport_step_profile_add.html', context)
    

   
    activity = Activity.objects.get(id = id)
    program = Program.objects.filter(id=activity.icn.program_id)
    current_user = request.user
    program_users = UserRoles.objects.filter(program__in=program, is_pcn_initiator=True)

    if User.objects.filter(id=current_user.id,userroles__in=program_users).exists():
        
        form = ActivityReportForm(user=current_user, activity=activity.id)   
        context = {'form':form, 'activity':activity, 'user':current_user}
        return render(request, 'report/activityreport_step_profile_add.html', context)
    
    return redirect('activity_step_approval',activity.id) 

@login_required(login_url='login')  
def activityreport_edit(request, id): 
    activity = Activity.objects.get(id=id)
    activityreport =  ActivityReport.objects.get(activity_id=id)
    
    if request.method == "POST":
       
        form = ActivityReportForm(request.POST, instance=activityreport, user=request.user)
        if form.is_valid():
            instance = form.save()
            selected_woredas = request.POST.getlist("aworeda")
            selected_co_agency = request.POST.getlist("alead_co_agency")
            items_woreda = ImplementationArea.objects.filter(id__in=selected_woredas)
            items_co_agency = Portfolio.objects.filter(id__in=selected_co_agency)
            instance.save()
            instance.aworeda.add(*items_woreda)
            instance.alead_co_agency.add(*items_co_agency)
            return redirect('activityreport_detail',id) 
            
        
        form = ActivityReportForm(request.POST,  instance=activityreport, user=request.user, activity=activity.id) 
        context = {'form':form, 'activity':activity, 'activityreport':activityreport}
        return render(request, 'report/activityreport_step_profile_add.html', context)
            
    current_user = request.user
    if current_user == activityreport.user and activityreport.status ==False:
        form = ActivityReportForm(instance=activityreport, user=current_user, activity=activity.id)   
        context = {'form':form, 'activity':activity, 'user':current_user}
        return render(request, 'report/activityreport_step_profile_add.html', context)
    
    return redirect('activityreport_detail',id) 
    
 
@login_required(login_url='login') 
def add_activityreport_impact(request, id):
    activityimpact = ActivityImpact.objects.get(pk=id)
    activity = Activity.objects.get(id=activityimpact.activity_id)
    
    
    activityreport = ActivityReport.objects.get(activity_id=activity.id)
    if request.method == "POST":
       
        form = ActivityReportImpactForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.activityimpact = activityimpact
            instance.activityreport = activityreport
            instance.save()
            
            
            if ActivityReportImpact.objects.filter(activityreport_id=instance.activityreport_id).count() == 1:
                return HttpResponseClientRedirect('/report/activity/'+str(activity.id)+'/impact/')
            else:
                return HttpResponse(
           
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "ImpactListChanged": None,
                        "showMessage": f"{instance.pk} updated."
                    })
                })
    else:
        form = ActivityReportImpactForm()
    return render(request, 'report/partial/activityreport_impact_form.html', {
        'form': form,
        'activityimpact': activityimpact,
    })

@login_required(login_url='login')    
def activityreport_impact_list(request, id):
    #impacts = Impact.objects.filter(icn_id=id)
    impacts=ActivityImpact.objects.filter(activity_id=id)
    context = {'impacts':impacts }
    return render(request, 'report/partial/activityreport_impact_list.html', context)


@login_required(login_url='login') 
def edit_activityreport_impact(request, pk):
    impact = get_object_or_404(ActivityReportImpact, pk=pk)
    activityreport = get_object_or_404(ActivityReport, pk=impact.activityreport_id)
    
   
    if request.method == "POST":
        impact = ActivityReportImpact.objects.get(pk=pk)
        form = ActivityReportImpactForm(request.POST, instance=impact)
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
        form = ActivityReportImpactForm(instance=impact)
    return render(request, 'report/partial/activityimpact_form_edit.html', {
        'form': form,
        'impact': impact,
    })

@login_required(login_url='login') 
def remove_activityreport_impact(request, pk):
    activityreport_impact = get_object_or_404(ActivityReportImpact, pk=pk)
    activityreport_impact.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "AImpactListChanged": None,
                "showMessage": f"{activityreport_impact.title} deleted."
            })
        })


@login_required(login_url='login') 
def search_results_view2(request):
    query = request.GET.get('search', '')
    

    all_activities= ActivityReport.objects.all()
    if query:
        qs1 = ActivityReport.objects.filter(title__icontains=query)
        qs2 = ActivityReport.objects.distinct().filter(icnreport__title__icontains=query)
        
        qs3 = ActivityReport.objects.distinct().filter(icnreport__program__title__icontains=query)
        activitiesreport = qs1.union(qs2, qs3).order_by('id')
       
    else:
        activitiesreport = all_activities

    context = {'activitiesreport': activitiesreport, 'count': activitiesreport.count()}
    return render(request, 'partial/activityreport_list.html', context)

@login_required(login_url='login') 
def activityreport_submit_approval(request, id):
    activity = Activity.objects.get(id=id)
    
 
    # add the dictionary during initialization
    activityreport = ActivityReport.objects.get(activity_id=activity.id)
    if ActivityReportSubmit.objects.filter(activityreport_id=activityreport.id).exists():
        activityreportsubmit = ActivityReportSubmit.objects.filter(activityreport_id=activityreport.id).latest('id')
        context = {'activity':activity, 'activityreport':activityreport, 'activityreportsubmit':activityreportsubmit}
    else:
        context = {'activity':activity, 'activityreport':activityreport}
    

    return render(request, 'report/activityreport_step_approval.html', context)


@login_required(login_url='login')  
def current_activityreport_submit_approval_list(request, id):
    context ={}
 
    # add the dictionary during initialization
  
    activity = Activity.objects.get(id=id)
    
    # add the dictionary during initialization
    activityreport = ActivityReport.objects.get(activity_id=activity.id)
    if ActivityReportSubmit.objects.filter(activityreport_id=activityreport.id).exists():
        activityreportsubmit = ActivityReportSubmit.objects.filter(activityreport_id=activityreport.id).latest('id')
        context = {'activity':activity, 'activityreport':activityreport, 'activityreportsubmit':activityreportsubmit}
    else:
        context = {'activity':activity, 'activityreport':activityreport}

    return render(request, 'report/partial/activityreport_submit_list.html', context)

@login_required(login_url='login') 
def activityreport_submit_form(request, id, sid): 
    activity = Activity.objects.get(id=id)
    activityreport = ActivityReport.objects.get(activity_id=activity.id)
    form = ActivityReportSubmitForm(sid=sid, activityreport=activityreport, user=request.user)
        
    if request.method == "POST":
        form = ActivityReportSubmitForm(request.POST, request.FILES, sid=sid)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.activityreport = activityreport
            
            instance.user = request.user
            instance.save()
            #document = IcnReportSubmit.objects.filter(icnreport_id=icnreport.id).latest('id')
            #document_i = Document.objects.filter(icnreport=instance.icnreport, user=icnreport.user).count()+1
            
            activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=instance.pk)
            #Document.objects.create(user = icnreport.user, document = instance.document,  icnreport=instance.icnreport, description = document_i)
            if activityreportsubmit.submission_status_id == 2:
                ActivityReport.objects.filter(activity_id=activity.id).update(status=True)
                ActivityReport.objects.filter(activity_id=activity.id).update(approval_status="Pending Approval")
                ActivityReportSubmitApproval_T.objects.create(user = activityreport.technical_lead,submit_id = instance, document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                ActivityReportSubmitApproval_P.objects.create(user = activityreport.program_lead,submit_id = instance,document = instance.document, approval_status=Approvalf_Status.objects.get(id=1))
                ActivityReportSubmitApproval_F.objects.create(user = activityreport.finance_lead,submit_id = instance,document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                ActivityReportSubmitApproval_M.objects.create(user = activityreport.mel_lead,submit_id = instance,document = instance.document, approval_status=Approvalt_Status.objects.get(id=1))
                send_activityreport_notify(activityreport.id, 12)
                return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
            
            elif activityreportsubmit.submission_status_id == 1:
                ActivityReport.objects.filter(activity_id=activity.id).update(status=False)
                ActivityReport.objects.filter(activity_id=activity.id).update(approval_status="Pending Submission'")
                send_activityreport_notify(activityreport.id, 11)

                return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
      
    context = {'form':form, 'activityreport':activityreport }
    return render(request, 'report/activityreport_submit_form.html', context)


@login_required(login_url='login') 
def activityreport_submit_document(request, id):
    context ={}
    activityreport = get_object_or_404(ActivityReport, pk=id)
    dform = ActivityReportDocumentForm()
    if ActivityReportDocument.objects.filter(activityreport=activityreport.id).exists():
        major = ActivityReportDocument.objects.filter(activityreport=activityreport.id, user=activityreport.user).count() 
        last_initiator_doc = ActivityReportDocument.objects.filter(activityreport=activityreport.id, user=activityreport.user).latest('id') 
        minor = ActivityReportDocument.objects.filter(activityreport=activityreport.id, id__gt=last_initiator_doc.id).exclude(user=activityreport.user)
        minor = minor.count()
    else:
        major = 0
        minor = 0

    context = {'dform':dform}
    if request.method == 'POST':
        dform = ActivityReportDocumentForm(request.POST, request.FILES)
        if dform.is_valid():
            instance = dform.save(commit=False)
            instance.activityreport = activityreport
            instance.user = request.user
            if instance.user == activityreport.user:
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
       dform = ActivityReportDocumentForm()
       context = {'dform':dform}
       return render(request, 'report/partial/activityreport_document_form.html', context)
           
@login_required(login_url='login')             
def activityreport_submit_form_partial(request, id): 
    activityreport = get_object_or_404(ActivityReport, pk=id)
    
    form = ActivityReportSubmitForm(user=request.user,activityreport=activityreport, sid=2)
    
    context = {'form':form, 'activityreport':activityreport}
    return render(request, 'report/partial/activityreport_partial_doc_form.html', context)

@login_required(login_url='login') 
def activityreport_document_list(request, id):
    documents = ActivityReportDocument.objects.filter(activityreport_id=id)
    context = {'documents':documents}
           
          
    
    return render(request,'report/partial/activityreport_document_list.html', context)

@login_required(login_url='login') 
def activityreport_submit_approval_list(request, id):
    activityreport_submit_list = ActivityReportSubmit.objects.filter(activityreport_id = id, submission_status=2)
    
    context = {'activityreport_submit_list': activityreport_submit_list }
    return render(request, 'report/partial/activityreport_submit_approval_list.html', context )


@login_required(login_url='login') 
def activityreport_approvalt(request, id, did):
     
    activityreportsubmitApproval_t = get_object_or_404(ActivityReportSubmitApproval_T, submit_id_id=id)
    activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=id)
    
    activityreport =  get_object_or_404(ActivityReport, id=activityreportsubmit.activityreport_id)

         
    if request.method == "GET":
        form = ActivityReportApprovalTForm(instance=activityreportsubmitApproval_t, user=request.user, activityreport=activityreport.id, did=did)
        
        context = {'activityreportsubmitapproval_t':activityreportsubmitApproval_t, 'form': form, 'activityreport':activityreport, 'did':did}
        return render(request, 'report/activityreport_approval_tform.html', context)
    
    elif request.method == "PUT":
        activityreportsubmitApproval_t = get_object_or_404(ActivityReportSubmitApproval_T, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = ActivityReportApprovalTForm(data, instance=activityreportsubmitApproval_t)
        if form.is_valid():
            instance =form.save()
           
            activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=id)
            activityreport =  get_object_or_404(ActivityReport, id=activityreportsubmit.activityreport_id)
            update_activityreport_approval_status(activityreportsubmit.id)
            send_activityreport_notify(activityreport.id, 2)

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'report/activityreport_approval_tform.html', {'form':form})

@login_required(login_url='login') 
def activityreport_approvalm(request, id, did):
     
    activityreportsubmitApproval_m = get_object_or_404(ActivityReportSubmitApproval_M , submit_id_id=id)
    activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=id)
    
    activityreport =  get_object_or_404(ActivityReport, id=activityreportsubmit.activityreport_id)

         
    if request.method == "GET":
        form = ActivityReportApprovalMForm(instance=activityreportsubmitApproval_m, user=request.user, activityreport=activityreport.id, did=did)
       
        
        context = {'activityreportsubmitapproval_m':activityreportsubmitApproval_m, 'form': form, 'activityreport':activityreport, 'did':did}
        return render(request, 'report/activityreport_approval_mform.html', context)
    
    elif request.method == "PUT":
        activityreportsubmitApproval_m = get_object_or_404(ActivityReportSubmitApproval_M, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = ActivityReportApprovalMForm(data, instance=activityreportsubmitApproval_m)
        if form.is_valid():
            instance =form.save()
           
            activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=id)
            activityreport =  get_object_or_404(ActivityReport, id=activityreportsubmit.activityreport_id)
            update_activityreport_approval_status(activityreportsubmit.id)
            send_activityreport_notify(activityreport.id, 3)

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'report/activityreport_approval_mform.html', {'form':form})

@login_required(login_url='login') 
def activityreport_approvalp(request, id, did):
     
    activityreportsubmitApproval_p = get_object_or_404(ActivityReportSubmitApproval_P, submit_id_id=id)
    activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=id)
    
    activityreport =  get_object_or_404(ActivityReport, id=activityreportsubmit.activityreport_id)

        
    if request.method == "GET":
        form = ActivityReportApprovalPForm(instance=activityreportsubmitApproval_p, user=request.user, activityreport=activityreport.id, did=did)
        
        context = {'activityreportsubmitapproval_p':activityreportsubmitApproval_p, 'form': form, 'activityreport':activityreport, 'did':did }
        return render(request, 'report/activityreport_approval_pform.html', context)
    
    elif request.method == "PUT":
        activityreportsubmitApproval_p = get_object_or_404(ActivityReportSubmitApproval_P, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = ActivityReportApprovalPForm(data, instance=activityreportsubmitApproval_p, did=did)
        if form.is_valid():
            instance =form.save()
            
            activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=id)
            activityreport =  get_object_or_404(ActivityReport, id=activityreportsubmit.activityreport_id)
            update_activityreport_approval_status_final(activityreportsubmit.id)
            send_activityreport_notify(activityreport.id, 5)
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'report/activityreport_approval_pform.html', {'form':form, 'did':did})

@login_required(login_url='login') 
def activityreport_approvalf(request, id, did):
     
    activityreportsubmitApproval_f = get_object_or_404(ActivityReportSubmitApproval_F, submit_id_id=id)
    activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=id)
    
    activityreport =  get_object_or_404(ActivityReport, id=activityreportsubmit.activityreport_id)

          
    if request.method == "GET":
        form = ActivityReportApprovalFForm(instance=activityreportsubmitApproval_f, user=request.user, activityreport=activityreport.id, did=did)
        

        context = {'activityreportsubmitapproval_f':activityreportsubmitApproval_f, 'form': form, 'activityreport':activityreport, 'did':did }
        return render(request, 'report/activityreport_approval_fform.html', context)
    
    elif request.method == "PUT":
        activityreportsubmitApproval_f = get_object_or_404(ActivityReportSubmitApproval_F, submit_id_id=id)
        data = QueryDict(request.body).dict()
        form = ActivityReportApprovalFForm(data, instance=activityreportsubmitApproval_f, did=did)
        if form.is_valid():
            instance =form.save()
            
            activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=id)
            activityreport =  get_object_or_404(ActivityReport, id=activityreportsubmit.activityreport_id)
            update_activityreport_approval_status(activityreportsubmit.id)
            send_activityreport_notify(activityreport.id, 4)

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "SubmitApprovalListChanged": None,
                        "showMessage": f"{instance.id} added."
                    })
                })
        
        return render(request, 'report/activityreport_approval_fform.html', {'form':form})

def update_activityreport_approval_status(id):
    activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=id)
    activityreportsubmitapproval_t = get_object_or_404(ActivityReportSubmitApproval_T, submit_id_id=id)
    activityreportsubmitapproval_m = get_object_or_404(ActivityReportSubmitApproval_M, submit_id_id=id)
    activityreportsubmitapproval_f = get_object_or_404(ActivityReportSubmitApproval_F, submit_id_id=id)
    
    approval_t = activityreportsubmitapproval_t.approval_status
    approval_t = int(approval_t)
    approval_m = activityreportsubmitapproval_m.approval_status
    approval_m = int(approval_m)
    approval_f = activityreportsubmitapproval_f.approval_status
    approval_f = int(approval_f)
    
    if approval_t == 4 or approval_m== 4 or approval_f== 4:
        ActivityReport.objects.filter(pk=activityreportsubmit.activityreport_id).update(approval_status="Rejected")
    if approval_t == 2 or approval_m== 2 or approval_f== 2:
        ActivityReport.objects.filter(pk=activityreportsubmit.activityreport_id).update(approval_status="Revision Required")
    elif approval_t == 1 and approval_m == 1 and approval_f == 1:
        ActivityReport.objects.filter(pk=activityreportsubmit.activityreport_id).update(approval_status="Pending Approval")
    elif approval_t == 3 and approval_m ==3 and approval_f==3:
        ActivityReport.objects.filter(pk=activityreportsubmit.activityreport_id).update(approval_status="75% Approved")
    elif (approval_t == 3 and approval_m ==3 and approval_f !=3) or (approval_t == 3 and approval_m !=3 and approval_f ==3) or (approval_t != 3 and approval_m ==3 and approval_f ==3):
        ActivityReport.objects.filter(pk=activityreportsubmit.activityreport_id).update(approval_status="50% Approved")
    elif (approval_t == 3 and approval_m !=3 and approval_f !=3) or (approval_t != 3 and approval_m ==3 and approval_f !=3) or (approval_t != 3 and approval_m!=3 and approval_f ==3):
        ActivityReport.objects.filter(pk=activityreportsubmit.activityreport_id).update(approval_status="25% Approved") 


def update_activityreport_approval_status_final(id):
    activityreportsubmit = get_object_or_404(ActivityReportSubmit, pk=id)
    activityreportsubmitapproval_p = get_object_or_404(ActivityReportSubmitApproval_P, submit_id_id=id)
    
    
    approval_p = activityreportsubmitapproval_p.approval_status
    approval_p = int(approval_p)
       
    if approval_p == 4:
        ActivityReport.objects.filter(pk=activityreportsubmit.activityreport_id).update(approval_status="Rejected")
    elif approval_p == 2:
        ActivityReport.objects.filter(pk=activityreportsubmit.activityreport_id).update(approval_status="Revision Required")
    elif approval_p == 3:
        ActivityReport.objects.filter(pk=activityreportsubmit.activityreport_id).update(approval_status="100% Approved")

@login_required(login_url='login') 
def downloada(request, id):
    document = get_object_or_404(ActivityReportDocument, id=id)
    response = HttpResponse(document.document, content_type='application/docx')
    response['Content-Disposition'] = f'attachment; filename="{document.document}"'
    return response

@login_required(login_url='login') 
def latest_submit_approval_list(request, id):
    if IcnReportSubmit.objects.filter(icn_id=id).exists():
         list = IcnReportSubmit.objects.filter(icn_id = id, submission_status=2).latest('id')
         context = {'list':list}
    else: 
        context = {}
    
    return render(request, 'partial/recent_submit_approval_list.html', context)

@login_required(login_url='login') 
def latest_submit_approval_list_activity(request, id):
    if ActivityReportSubmit.objects.filter(activity_id = id).exists():
        list = ActivityReportSubmit.objects.filter(activity_id = id, submission_status=2).latest('id')
        context = {'list':list}
    else: 
        context = {}
    return render(request, 'report/partial/recent_submit_approval_list_activity.html', context)


def send_icnreport_notify(id, uid):
    icnreport = get_object_or_404(IcnReport, id=id)
    if uid == 12:
        subject = 'Request for ICN Report Approval'
        initiator = icnreport.user.profile.full_name
        user_role = 'Initiator'
    elif uid == 11:
        subject = 'ICN Report Approval Request temporarily withdrawn'
        initiator = icnreport.user.profile.full_name
        user_role = 'Initiator'
        
    elif uid ==2:
        subject = 'ICN Report Approval Status changed'
        initiator = icnreport.technical_lead.user.profile.full_name
        user_role = 'Technical Lead'
    elif uid ==3:
        subject = 'ICN Report Approval Status changed'
        initiator = icnreport.mel_lead.user.profile.full_name
        user_role = 'MEL Lead'
    elif uid ==4:
        subject = 'ICN Report Approval Status changed'
        initiator = icnreport.finance_lead.user.profile.full_name
        user_role = 'Finance Lead'
    elif uid ==5:
        subject = 'ICN Report Final Approval Status changed'
        initiator = icnreport.program_lead.user.profile.full_name
        user_role = 'Program Lead'
        

    subject = subject
    context = {
                "program": icnreport.icn.program,
                "title": icnreport.icn.title,
                "id": icnreport.icn.id,
                "cn_id": icnreport.icn.icn_number,
                "creator": icnreport.user.profile.full_name,
                "initiator": initiator,
                "user_role": user_role,
            
                
                }
    html_message = render_to_string("report/partial/report_mail.html", context=context)
    plain_message = strip_tags(html_message)
    recipient_list = [icnreport.user.email, icnreport.mel_lead.user.email, icnreport.technical_lead.user.email,  icnreport.finance_lead.user.email]
        
    message = EmailMultiAlternatives(
        subject = subject, 
        body = plain_message,
        from_email = None ,
        to= recipient_list
            )
        
    message.attach_alternative(html_message, "text/html")
    message.send()
    
    if uid !=5 and icnreport.approval_status == '75% Approved':
        subject = 'Request for ICN Report Final Approval'
        html_message = render_to_string("report/partial/report_mail.html", context=context)
        plain_message = strip_tags(html_message)
        recipient_list = [icnreport.user.email, icnreport.technical_lead.user.email, icnreport.mel_lead.user.email ,icnreport.program_lead.user.email, icnreport.finance_lead.user.email]
        
        message = EmailMultiAlternatives(
            subject = subject, 
            body = plain_message,
            from_email = None ,
            to= recipient_list
                )
        
        message.attach_alternative(html_message, "text/html")
        message.send()


def send_activityreport_notify(id, uid):
    activityreport = get_object_or_404(ActivityReport, id=id)
    if uid == 12:
        subject = 'Request for ACN Report Approval'
        initiator = activityreport.user.profile.full_name
        user_role = 'Initiator'
    elif uid == 11:
        subject = 'ACN Report Approval Request temporarily withdrawn'
        initiator = activityreport.user.profile.full_name
        user_role = 'Initiator'
        
    elif uid ==2:
        subject = 'ACN Report Approval Status changed'
        initiator = activityreport.technical_lead.user.profile.full_name
        user_role = 'Technical Lead'
    elif uid ==3:
        subject = 'ACN Report Approval Status changed'
        initiator = activityreport.mel_lead.user.profile.full_name
        user_role = 'MEL Lead'
    elif uid ==4:
        subject = 'ACN Report Approval Status changed'
        initiator = activityreport.finance_lead.user.profile.full_name
        user_role = 'Finance Lead'
    elif uid ==5:
        subject = 'ACN Report Final Approval Status changed'
        initiator = activityreport.program_lead.user.profile.full_name
        user_role = 'Program Lead'
        

    subject = subject
    context = {
                "program": activityreport.activity.icn.program,
                "title": activityreport.activity.title,
                "id": activityreport.activity.id,
                "cn_id": activityreport.activity.acn_number,
                "creator": activityreport.user.profile.full_name,
                "initiator": initiator,
                "user_role": user_role,
            
                
                }
    html_message = render_to_string("report/partial/activityreport_mail.html", context=context)
    plain_message = strip_tags(html_message)
    recipient_list = [activityreport.user.email, activityreport.mel_lead.user.email, activityreport.technical_lead.user.email,  activityreport.finance_lead.user.email]
        
    message = EmailMultiAlternatives(
        subject = subject, 
        body = plain_message,
        from_email = None ,
        to= recipient_list
            )
        
    message.attach_alternative(html_message, "text/html")
    message.send()
    
    if uid !=5 and activityreport.approval_status == '75% Approved':
        subject = 'Request for ACN Report Final Approval'
        html_message = render_to_string("report/partial/activityreport_mail.html", context=context)
        plain_message = strip_tags(html_message)
        recipient_list = [activityreport.user.email, activityreport.technical_lead.user.email, activityreport.mel_lead.user.email ,activityreport.program_lead.user.email, activityreport.finance_lead.user.email]
        
        message = EmailMultiAlternatives(
            subject = subject, 
            body = plain_message,
            from_email = None ,
            to= recipient_list
                )
        
        message.attach_alternative(html_message, "text/html")
        message.send()