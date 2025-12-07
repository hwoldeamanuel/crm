from django.db import models
from program.models import Program
from django.contrib.auth.models import User
from portfolio.models import Portfolio
from app_admin.models import Feedback_Channel, Feedback_Category, Informant_Gender, Informant_Age, FieldOffice, Informed_Consent, Informant_Status, Region, Zone, Woreda, Feedback_Status, Feedback_Response_Type, Feedback_Resolution
# Create your models here.
import os

def path_and_rename(instance, filename):
    upload_to = 'documents/'
    ext = filename.split('.')[-1]

    filename = '{}.{}'.format(instance.id, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Feedback(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)
    partner = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING)
    date_feedback_recieved= models.DateField( null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    feedback_channel = models.ForeignKey(Feedback_Channel, on_delete=models.DO_NOTHING, null=True, blank=True)
    feedback_channel_other = models.TextField(null=True, blank=True)
    feedback_category = models.ForeignKey(Feedback_Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    supporting_document = models.FileField(null=True,  blank=True, upload_to=path_and_rename)
    office_location = models.ForeignKey(FieldOffice, on_delete=models.DO_NOTHING, null=True, blank=True)
    informed_consent = models.ForeignKey(Informed_Consent, on_delete=models.DO_NOTHING, null=True, blank=True)
    informant_status = models.ForeignKey(Informant_Status, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    informant_name = models.TextField(null=True, blank=True)
    informant_sex  = models.ForeignKey(Informant_Gender, on_delete=models.DO_NOTHING, null=True, blank=True)
    informant_age  = models.ForeignKey(Informant_Age, on_delete=models.DO_NOTHING, null=True, blank=True)
    informant_location = models.ForeignKey(Woreda, on_delete=models.DO_NOTHING, null=True, blank=True)
    informant_location_other = models.TextField(null=True, blank=True)
    informant_contact_phone_number = models.TextField(null=True, blank=True)
    informant_contact_other = models.TextField(null=True, blank=True)
    feedback_Status = models.ForeignKey(Feedback_Status, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='feedback_updated_by')

    class Meta:
        ordering = ('-published_date',)
    
    def __str__(self):
        return str(self.id)
    
   
    def feedback_status(self):
         if Closing.objects.filter(feedback =self).exists():
             status =  "Closed"
         elif Processing.objects.filter(feedback =self).exists():
             status =  "In Progress"   
         else: status = "Pending"
         
         return status



class Processing(models.Model):
    Yes = 1
    No = 2
    Yes_No =   (
        (Yes, 'Yes'),
        (No, 'No'),
     
        )
    Internally = 1
    Externally = 2
    shared_to =   (
        (Internally, 'Internally'),
        (Externally, 'Externally'),
     
        )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    feedback = models.OneToOneField(Feedback, on_delete=models.CASCADE, null=True, blank=True)
    processing_date = models.DateField( null=True,   blank=True)
    feedback_referred = models.PositiveSmallIntegerField(choices=Yes_No, default=1,  blank=True, null=True)
    feedback_shared = models.PositiveSmallIntegerField(choices=Yes_No,  default=1,  blank=True, null=True)
    feedback_shared_with = models.PositiveSmallIntegerField(choices=shared_to, blank=True, null=True)
    feedback_shared_with_note = models.TextField(null=True, blank=True)
    feedback_referred_to = models.TextField(null=True, blank=True)
   
    types_of_response_required = models.ForeignKey(Feedback_Response_Type, on_delete=models.DO_NOTHING, null=True, blank=True)
    types_of_response_required_other = models.TextField(null=True, blank=True)
   
    action_followup_needed = models.PositiveSmallIntegerField(choices=Yes_No,  default=1,  blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='processing_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)
  

    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.id)
    
class Closing(models.Model):
    Yes = 1
    No = 2
    Yes_No =   (
        (Yes, 'Yes'),
        (No, 'No'),
     
        )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    feedback = models.OneToOneField(Feedback, on_delete=models.CASCADE, null=True, blank=True)
    action_taken =models.ForeignKey(Feedback_Response_Type, on_delete=models.DO_NOTHING, null=True, blank=True)
    action_taken_other = models.TextField(null=True, blank=True)
    action_taken_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='action_taken_by')
    
    responses_provided = models.PositiveSmallIntegerField(choices=Yes_No, default=1,  blank=True, null=True)
    response_date = models.DateField(null=True, blank=True)
    response_summary = models.TextField(null=True, blank=True)
    resolution = models.ForeignKey(Feedback_Resolution, on_delete=models.DO_NOTHING, null=True, blank=True)
    feedback_closed = models.PositiveSmallIntegerField(choices=Yes_No, default=1,  blank=True, null=True)
    closing_date = models.DateField( null=True,   blank=True)
    feedback_checked_reviewed = models.BooleanField(default=False)
    date_reviewed = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='closing_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)
  
    
    class Meta:
        ordering = ('-closing_date',)

    def __str__(self):
        return str(self.id)