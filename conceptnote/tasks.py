# tasks.py


from .models import Icn, Activity, IcnSubmit, IcnSubmitApproval_F,IcnSubmitApproval_T, IcnSubmitApproval_P, IcnSubmitApproval_M, ActivitySubmit, ActivitySubmitApproval_M, ActivitySubmitApproval_F, ActivitySubmitApproval_P, ActivitySubmitApproval_T
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from django.db.models.functions import ExtractDay
from django.utils import timezone
from django.db.models import F

def remainder():
    pending_icns = Icn.objects.filter(status=True).exclude(approval_status='100% Approved')

    for icn in pending_icns:
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        id = icnsubmit.id
        

        recipient_list = [icn.user.email]
        icnsubmitApproval_t = get_object_or_404(IcnSubmitApproval_T, submit_id_id=id)
        days_overdue_t= ExtractDay(timezone.now().date() - F(icnsubmitApproval_t.approval_date))
        icnsubmitApproval_m = get_object_or_404(IcnSubmitApproval_M, submit_id_id=id)
        days_overdue_m= ExtractDay(timezone.now().date() - F(icnsubmitApproval_m.approval_date))
        icnsubmitApproval_f = get_object_or_404(IcnSubmitApproval_F, submit_id_id=id)
        days_overdue_f= ExtractDay(timezone.now().date() - F(icnsubmitApproval_f.approval_date))
        

        if icnsubmitApproval_t.approval_status == 1 and days_overdue_t > 2:
            recipient_list.append(icnsubmitApproval_t.user.user.email)
        if icnsubmitApproval_m.approval_status == 1 and days_overdue_m > 2:
            recipient_list.append(icnsubmitApproval_m.user.user.email)
        if icnsubmitApproval_f.approval_status == 1 and days_overdue_f > 2:
            recipient_list.append(icnsubmitApproval_f.user.user.email)
            
        
        if len(recipient_list)>1:
            subject = 'Request for Approval'
            context = {
                        "program": icn.program,
                        "title": icn.title,
                        "id": icn.id,
                        "cn_id": icn.icn_number,
                        "creator": icn.user.profile.full_name,
                        "initiator": icn.user.profile.full_name,
                        "user_role": "Concept Note Initiator",
                       
                        "date": icnsubmit.submission_date,
                        }
                
            html_message = render_to_string("partial/intervention_mail.html", context=context)
            plain_message = strip_tags(html_message)
       
        
            message = EmailMultiAlternatives(
            subject = subject, 
            body = plain_message,
            from_email = 'Mercy Corps ETH CNMS',
            to= recipient_list
                )
            
            message.attach_alternative(html_message, "text/html")
            message.send()

    pending_icns_p = Icn.objects.filter(status=True).exclude(approval_status='100% Approved')

    for icn in pending_icns_p:
        icnsubmit = IcnSubmit.objects.filter(icn_id=icn.id).latest('id')
        id = icnsubmit.id
        

        icnsubmitApproval_p = get_object_or_404(IcnSubmitApproval_P, submit_id_id=id)
        days_overdue_p= ExtractDay(timezone.now().date() - F(icnsubmitApproval_p.approval_date))

        if icnsubmitApproval_p.approval_status == 1 and days_overdue_p > 2:
            recipient_list = [icn.user.email, icnsubmitApproval_p.user.user.email]
            
            subject = 'Request for Final Approval'
            context = {
                        "program": icn.program,
                        "title": icn.title,
                        "id": icn.id,
                        "cn_id": icn.icn_number,
                        "creator": icn.user.profile.full_name,
                        "initiator": icn.user.profile.full_name,
                        "user_role": "Concept Note Initiator",
                       
                        "date": icnsubmit.submission_date,
                        }
                
            html_message = render_to_string("partial/intervention_mail.html", context=context)
            plain_message = strip_tags(html_message)
        
            
            message = EmailMultiAlternatives(
            subject = subject, 
            body = plain_message,
            from_email = 'Mercy Corps ETH CNMS',
            to= recipient_list
                )
            
            message.attach_alternative(html_message, "text/html")
            message.send()

    pending_acns = Activity.objects.filter(status=True).exclude(approval_status='100% Approved')

    for acn in pending_acns:
        acnsubmit = ActivitySubmit.objects.filter(activity_id=acn.id).latest('id')
        id = acnsubmit.id
        

        recipient_list = [icn.user.email]
        acnsubmitApproval_t = get_object_or_404(ActivitySubmitApproval_T, submit_id_id=id)
        days_overdue_t= ExtractDay(timezone.now().date() - F(acnsubmitApproval_t.approval_date))
        acnsubmitApproval_m = get_object_or_404(ActivitySubmitApproval_M, submit_id_id=id)
        days_overdue_m= ExtractDay(timezone.now().date() - F(acnsubmitApproval_m.approval_date))
        acnsubmitApproval_f = get_object_or_404(ActivitySubmitApproval_F, submit_id_id=id)
        days_overdue_f= ExtractDay(timezone.now().date() - F(acnsubmitApproval_f.approval_date))
        

        if acnsubmitApproval_t.approval_status == 1 and days_overdue_t > 2:
            recipient_list.append(acnsubmitApproval_t.user.user.email)
        if acnsubmitApproval_m.approval_status == 1 and days_overdue_m > 2:
            recipient_list.append(acnsubmitApproval_m.user.user.email)
        if acnsubmitApproval_f.approval_status == 1 and days_overdue_f > 2:
            recipient_list.append(acnsubmitApproval_f.user.user.email)
            
        
        if len(recipient_list)>1:
            subject = 'Request for Approval'
            context = {
                        "program": acn.icn.program,
                        "title": acn.title,
                        "id": acn.id,
                        "cn_id": acn.acn_number,
                        "creator": acn.user.profile.full_name,
                        "initiator": acn.user.profile.full_name,
                        "user_role": "Concept Note Initiator",
                       
                        "date": acnsubmit.submission_date,
                        }
                
            html_message = render_to_string("partial/activity_mail.html", context=context)
            plain_message = strip_tags(html_message)
       
        
            message = EmailMultiAlternatives(
            subject = subject, 
            body = plain_message,
            from_email = 'Mercy Corps ETH CNMS',
            to= recipient_list
                )
            
            message.attach_alternative(html_message, "text/html")
            message.send()

    pending_acns_p = Activity.objects.filter(status=True).exclude(approval_status='100% Approved')

    for acn in pending_acns_p:
        acnsubmit = ActivitySubmit.objects.filter(activity_id=acn.id).latest('id')
        id = acnsubmit.id
    
       
        acnsubmitApproval_p = get_object_or_404(ActivitySubmitApproval_P, submit_id_id=id)
        days_overdue_p= ExtractDay(timezone.now().date() - F(acnsubmitApproval_p.approval_date))

        if acnsubmitApproval_p.approval_status == 1 and days_overdue_p > 2:
            recipient_list = [acn.user.email, acnsubmitApproval_p.user.user.email]
            
            subject = 'Request for Final Approval'
            context = {
                        "program": acn.icn.program,
                        "title": acn.title,
                        "id": acn.id,
                        "cn_id": acn.icn_number,
                        "creator": acn.user.profile.full_name,
                        "initiator": acn.user.profile.full_name,
                        "user_role": "Concept Note Initiator",
                       
                        "date": acnsubmit.submission_date,
                        }
                
            html_message = render_to_string("partial/activity_mail.html", context=context)
            plain_message = strip_tags(html_message)
        
            
            message = EmailMultiAlternatives(
            subject = subject, 
            body = plain_message,
            from_email = 'Mercy Corps ETH CNMS',
            to= recipient_list
                )
            
            message.attach_alternative(html_message, "text/html")
            message.send()


 