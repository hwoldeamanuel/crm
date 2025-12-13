from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm, ProcessingForm, ClosingForm
from .models import Feedback, Processing, Closing
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage


@login_required(login_url='login')
def carm(request):
    feedbacks = Feedback.objects.all()
    #icns = Icn.objects.all()
    

    context = {'feedbacks':feedbacks}
    
    return render(request, 'carm.html', context)



@login_required(login_url='login')
def feedback_add(request):
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            instance = form.save()
            send_notify(instance.pk)
            return redirect('feedback_detail',instance.pk) 
        
        form = FeedbackForm(request.POST, request.FILES)
        context = {'form':form}
        return render(request, 'feedback_new.html', context)
        
        
    context = {'form':form}
    return render(request, 'feedback_new.html', context)



@login_required(login_url='login')
def feedback_detail(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    

    

    context = { 'feedback':feedback}
    
    return render(request, 'feedback_detail.html', context)



@login_required(login_url='login')
def feedback_edit(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    form = FeedbackForm(instance=feedback)
    if request.method == 'POST':
        form = FeedbackForm(request.POST,request.FILES, instance=feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            instance = form.save()
            return redirect('feedback_detail',instance.pk) 
        
        form = FeedbackForm(request.POST, request.FILES, instance=feedback)
        context = {'form':form, 'feedback':feedback}
        return render(request, 'feedback_new.html', context)

    
    context = {'form':form, 'feedback':feedback}
    
    return render(request, 'feedback_new.html', context)

@login_required(login_url='login')
def feedback_processing_add(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    form = ProcessingForm()
    if request.method == 'POST':
        form = ProcessingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.feedback = feedback
            instance.save()
            instance = form.save()
            return redirect('feedback_processing',instance.feedback_id)
        
        form = ProcessingForm(request.POST)
        context = {'form':form, }
        return render(request, 'feedback_processing_edit.html', context)

    context = {'form': form, 'feedback':feedback}
    
    return render(request, 'feedback_processing_edit.html', context)

@login_required(login_url='login')
def feedback_processing(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    processing = get_object_or_404(Processing, feedback_id=feedback.id)
    

    
#
    context = {'processing':processing, 'feedback':feedback}
    
    return render(request, 'feedback_processing.html', context)


def emailbar(request):
    return render(request, 'email.html')


@login_required(login_url='login')
def download_feedback_att(request, id):
    document = get_object_or_404(Feedback, id=id)
   
    response = HttpResponse(document.supporting_document, content_type='application/docx')
    response['Content-Disposition'] = f'attachment; filename="{document.supporting_document}"'
    return response

def feedback_processing_edit(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    processing = get_object_or_404(Processing, feedback_id=feedback.id)
    
    form = ProcessingForm(instance=processing)
    if request.method == 'POST':
        form = ProcessingForm(request.POST, instance=processing)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.feedback = feedback
            instance.save()
           
            return redirect('feedback_processing',instance.feedback_id)
        
        form = ProcessingForm(request.POST, instance=processing)
        context = {'form':form, }
        return render(request, 'feedback_processing.html', context)
    

    context = {'form':form,'processing':processing, 'feedback':feedback}
    
    return render(request, 'feedback_processing_edit.html', context)


def emailbar(request):
    return render(request, 'email.html')



@login_required(login_url='login')
def feedback_closing_add(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    form = ClosingForm()
    if request.method == 'POST':
        form = ClosingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.feedback = feedback
            instance.save()
            
            return redirect('feedback_closing',instance.feedback_id)
        
        form = ClosingForm(request.POST)
        context = {'form':form, }
        return render(request, 'feedback_closing_new.html', context)
     
#
    context = {'form':form, 'feedback':feedback}
    
    return render(request, 'feedback_closing_new.html', context)


@login_required(login_url='login')
def feedback_closing(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    closing = get_object_or_404(Closing, feedback_id=feedback.id)
    if request.method == 'POST':
        form = ClosingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.feedback = feedback
            instance.save()
            instance = form.save()
            return redirect('feedback_closing',instance.feedback_id)
        
        form = ClosingForm(request.POST)
        context = {'form':form, }
        return render(request, 'feedback_closing.html', context)
     
#
    context = {'closing':closing, 'feedback':feedback}
    
    return render(request, 'feedback_closing.html', context)


@login_required(login_url='login')
def feedback_closing_edit(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    closing = get_object_or_404(Closing, feedback_id=feedback.id)
    form = ClosingForm(instance=closing)
    if request.method == 'POST':
        form = ClosingForm(request.POST, instance=closing)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.feedback = feedback
            instance.save()
            
            return redirect('feedback_closing',instance.feedback_id)
        
        form = ClosingForm(request.POST)
        context = {'form':form, }
        return render(request, 'feedback_closing_new.html', context)
     
#
    context = {'form':form, 'feedback':feedback}
    
    return render(request, 'feedback_closing_new.html', context)


def send_notify(id):
    
    feedback = get_object_or_404(Feedback, id=id)
    
        

    subject = 'New CARM Feedback has been submitted'
    context = {
                "program": feedback.program,
                "title": feedback.feedback_category,
                "id": feedback.id,
               
                "creator": feedback.user.profile.full_name,
                "last_modified": feedback.updated_by,
                
            
                
                }
    html_message = render_to_string("feedback_mail.html", context=context)
    plain_message = strip_tags(html_message)
    recipient_list = [feedback.user.email,]
        
    message = EmailMessage(
        subject = subject, 
        body = plain_message,
        from_email = 'Mercy Corps CARM',
        to= recipient_list
            )
    
    message.send()